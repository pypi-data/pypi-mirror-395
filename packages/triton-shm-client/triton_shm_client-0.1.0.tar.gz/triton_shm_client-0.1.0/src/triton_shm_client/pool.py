from multiprocessing import shared_memory
import queue
import uuid
from typing import List, Tuple, Dict, Any

import numpy as np


class SHMSlot:
    """
    Internal helper. Represents one 'unit' of work within the SharedMemoryPool
    Contains pre-calculated numpy views into the raw SHM buffer.
    """

    def __init__(
        self,
        region_name: str,
        shm_buffer: Any,
        input_specs: List[Tuple[str, Tuple[int, ...], np.dtype]],
        output_specs: List[Tuple[str, Tuple[int, ...], np.dtype]],
        slot_offset: int,
    ):
        self.region_name = region_name  # The name registered with Triton
        self.offset = slot_offset  # Offset of this slot within the region

        self.input_maps: Dict[str, np.ndarray] = {}  # {name: np_view}
        self.output_maps: Dict[str, np.ndarray] = {}  # {name: np_view}
        self.input_meta: List[Tuple[str, int, int]] = (
            []
        )  # List of (name, max_byte_size, relative_offset)
        self.output_meta: List[Tuple[str, int, int]] = (
            []
        )  # List of (name, max_byte_size, relative_offset)

        current_local_offset = slot_offset

        # 1. Map inputs
        for name, shape, dtype in input_specs:
            # create numpy view into SHM
            view = np.ndarray(
                shape,
                dtype=dtype,
                buffer=shm_buffer,
                offset=current_local_offset,
            )
            self.input_maps[name] = view

            byte_size = view.nbytes
            # Store metadata for Triton GRPC calls
            # Note: We store the offset relative to the Region start, which is
            # needed by Triton
            self.input_meta.append((name, byte_size, current_local_offset))

            current_local_offset += byte_size

        # 2. Map outputs
        for name, shape, dtype in output_specs:
            view = np.ndarray(
                shape,
                dtype=dtype,
                buffer=shm_buffer,
                offset=current_local_offset,
            )
            self.output_maps[name] = view

            byte_size = view.nbytes
            self.output_meta.append((name, byte_size, current_local_offset))
            current_local_offset += byte_size


class SHMModelContext:
    """
    Manages the lifecycle of the Shared Memory Region for a specific model.
    Under the hood creates a single large shared memory region divided into
    multiple slots based on the pool size. Each slot contains pre-allocated
    input and output buffers. 1 slot can handle 1 inference request (with
    batching up to max_batch_size).
    """

    def __init__(
        self,
        model_name: str,
        inputs: List[Tuple[str, Tuple[int, ...], np.dtype]],
        outputs: List[Tuple[str, Tuple[int, ...], np.dtype]],
        max_batch_size: int,
        pool_size: int,
    ):
        """
        :param model_name: The name of the model.
        :type model_name: str
        :param inputs: A list of input specifications for the model. Each
            specification is a tuple containing
            (input_name, input_shape, input_dtype) where `input_shape` does
            not include batch dimension.
        :type inputs: List[Tuple[str, Tuple[int, ...], np.dtype]]
        :param outputs: A list of output specifications for the model. Each
            specification is a tuple containing
            (output_name, output_shape, output_dtype) where `output_shape`
            does not include batch dimension.
        :type outputs: List[Tuple[str, Tuple[int, ...], np.dtype]]
        :param max_batch_size: The maximum batch size supported by the model.
            Can be a smaller value.
        :type max_batch_size: int
        :param pool_size: The size of the shared memory pool for the model.
            Acts as the number of concurrent slots.
        :type pool_size: int
        """
        if max_batch_size <= 0:
            raise ValueError("max_batch_size must be greater than 0")
        if pool_size <= 0:
            raise ValueError("pool_size must be greater than 0")

        self.model_name = model_name
        self.max_batch_size = max_batch_size
        self.pool = queue.LifoQueue()  # Lifo queue for better cache locality

        # 1. Calculate sizes
        # inputs/outputs are list of tuples (name, base_shape, dtype)
        # we need to expand base_shape to (max_batch_size, *base_shape)

        self.input_specs: List[Tuple[str, Tuple[int, ...], np.dtype]] = []
        self.output_specs: List[Tuple[str, Tuple[int, ...], np.dtype]] = []

        slot_size_bytes = 0

        def shape_valid(shape: Tuple[int, ...]) -> bool:
            for dim in shape:
                if dim <= 0:
                    return False
            return True

        for name, base_shape, dtype in inputs:
            if not shape_valid(base_shape):
                raise ValueError(
                    f"Invalid input shape {base_shape} for input {name}"
                )
            full_shape = (max_batch_size, *base_shape)
            byte_size = int(np.prod(full_shape) * np.dtype(dtype).itemsize)
            self.input_specs.append((name, full_shape, dtype))
            slot_size_bytes += byte_size

        for name, base_shape, dtype in outputs:
            if not shape_valid(base_shape):
                raise ValueError(
                    f"Invalid output shape {base_shape} for output {name}"
                )
            full_shape = (max_batch_size, *base_shape)
            byte_size = int(np.prod(full_shape) * np.dtype(dtype).itemsize)
            self.output_specs.append((name, full_shape, dtype))
            slot_size_bytes += byte_size

        # Align to 64 bytes
        if slot_size_bytes % 64 != 0:
            slot_size_bytes += 64 - (slot_size_bytes % 64)

        # 2. Allocate OS shared memory
        total_region_size = slot_size_bytes * pool_size
        self.unique_shm_name = f"{model_name}_{uuid.uuid4().hex[:8]}"

        try:
            self.shm = shared_memory.SharedMemory(
                create=True, size=total_region_size, name=self.unique_shm_name
            )
        except FileExistsError:
            # Cleanup stale handle if exists and retry
            # (rare collision of unclean exit)
            s = shared_memory.SharedMemory(name=self.unique_shm_name)
            s.close()
            s.unlink()

            self.shm = shared_memory.SharedMemory(
                create=True, size=total_region_size, name=self.unique_shm_name
            )

        # 4. Create Slots and populate pool
        for i in range(pool_size):
            offset = i * slot_size_bytes
            slot = SHMSlot(
                self.unique_shm_name,
                self.shm.buf,
                self.input_specs,
                self.output_specs,
                offset,
            )
            self.pool.put(slot)

    @property
    def shm_name(self) -> str:
        """The name of the shared memory region."""
        return self.unique_shm_name

    @property
    def shm_size(self) -> int:
        """The size of the shared memory region in bytes."""
        if self.shm is None:
            return 0
        return self.shm.size

    def destroy(self) -> None:
        """Cleans up the shared memory region."""
        try:
            self.shm.close()
            self.shm.unlink()
        except FileNotFoundError:
            pass

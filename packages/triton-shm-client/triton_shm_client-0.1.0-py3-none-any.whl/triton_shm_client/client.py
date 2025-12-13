import atexit
import threading
from functools import partial
from typing import Any, Dict, List, Tuple, Union
import logging

import tritonclient.grpc as grpcclient
from tritonclient.utils import np_to_triton_dtype
import numpy as np

from .pool import SHMModelContext, SHMSlot

logger = logging.getLogger(__name__)


class TritonSHMClient(grpcclient.InferenceServerClient):
    """
    A client for Triton Inference Server that exposes a simpler interface for
    high-throughput inference using shared memory pools for input and output
    data. Requires Triton Inference Server to be colocated with the client
    process.
    """

    def __init__(
        self,
        url: str,
        verbose: bool = False,
        ssl: bool = False,
        root_certificates: Any | None = None,
        private_key: Any | None = None,
        certificate_chain: Any | None = None,
        creds: Any | None = None,
        keepalive_options: Any | None = None,
        channel_args: Any | None = None,
    ):
        super().__init__(
            url=url,
            verbose=verbose,
            ssl=ssl,
            root_certificates=root_certificates,
            private_key=private_key,
            certificate_chain=certificate_chain,
            creds=creds,
            keepalive_options=keepalive_options,
            channel_args=channel_args,
        )

        self.registered_models: Dict[str, SHMModelContext] = {}

        # Safety: ensure cleanup if script exists suddenly
        atexit.register(self.cleanup_all_shm)

    def close(self) -> None:
        """
        Closes the client and cleans up all registered shared memory pools.
        Any future calls to the server will result in an Error.
        """
        self.cleanup_all_shm()
        super().close()

    def register_shm_model(
        self,
        model_name: str,
        inputs: List[Tuple[str, Tuple[int, ...], np.dtype]],
        outputs: List[Tuple[str, Tuple[int, ...], np.dtype]],
        max_batch_size: int,
        pool_size: int,
    ) -> None:
        """
        Registers a model with a shared memory pool for high-throughput
        inference.
        Using this method pre-allocates shared memory regions for inputs and
        outputs and registers them with Triton Inference Server. The client
        can then perform inference using the pre-allocated shared memory
        regions.

        :param model_name: The name of the model to register.
        :type model_name: str
        :param inputs: A list of input specifications for the model. Each
            specification is a tuple containing the
            (input_name, shape, dtype), where shape is a tuple representing
            the shape of the input tensor EXCLUDING the batch dimension.
        :type inputs: List[Tuple[str, Tuple[int, ...], np.dtype]]
        :param outputs: A list of output specifications for the model. Each
            specification is a tuple containing the
            (output_name, shape, dtype), where shape is a tuple representing
            the shape of the output tensor EXCLUDING the batch dimension.
        :type outputs: List[Tuple[str, Tuple[int, ...], np.dtype]]
        :param max_batch_size: The maximum batch size the model supports.
            Can be smaller than the model's max batch size. If the
            `max_batch_size` exceeds the model's max batch size, on inference
            an error will be raised by Triton.
        :type max_batch_size: int
        :param pool_size: The size of the shared memory pool to allocate
            for the model. This determines how many concurrent inference
            requests can be handled using shared memory.
        :type pool_size: int
        """
        if model_name in self.registered_models:
            raise ValueError(
                f"Model {model_name} is already registered. Unregister first."
            )

        ctx = SHMModelContext(
            model_name, inputs, outputs, max_batch_size, pool_size
        )

        try:
            self.register_system_shared_memory(
                name=ctx.shm_name, key=ctx.shm_name, byte_size=ctx.shm_size
            )
        except Exception as e:
            ctx.destroy()
            raise e

        self.registered_models[model_name] = ctx
        logger.info(
            f"Registered model {model_name} with SHM region "
            f"{ctx.shm_name} of size {ctx.shm_size} bytes."
        )

    def unregister_shm_model(self, model_name: str) -> None:
        """
        Unregisters a model and cleans up its shared memory pool.

        :param model_name: The name of the model to unregister.
        :type model_name: str
        """
        if model_name not in self.registered_models:
            logger.warning(
                f"Attempted to unregister nonexistent model: {model_name}"
            )
            return

        ctx = self.registered_models[model_name]
        try:
            self.unregister_system_shared_memory(ctx.shm_name)
        except Exception as e:
            logger.warning(
                f"Failed to unregister SHM for model {model_name}: {e}"
            )
        finally:
            ctx.destroy()
            del self.registered_models[model_name]

    def cleanup_all_shm(self) -> None:
        """
        Unregisters all models and cleans up their shared memory pools.
        """
        keys = list(self.registered_models.keys())
        for k in keys:
            self.unregister_shm_model(k)

    def infer_shm(
        self,
        model_name: str,
        inputs: Dict[str, Union[np.ndarray, List[np.ndarray]]],
        model_version: str = "",
        request_id: str = "",
        sequence_id: int = 0,
        sequence_start: bool = False,
        sequence_end: bool = False,
        priority: int = 0,
        timeout: Any | None = None,
        client_timeout: Any | None = None,
        headers: Any | None = None,
        compression_algorithm: Any | None = None,
        parameters: Any | None = None,
    ) -> Dict[str, np.ndarray]:
        """
        Performs inference using shared memory for input and output data.
        This method handles batching of input data, writing inputs to
        shared memory, and reading outputs from shared memory after inference
        is complete.
        Uses asynchronous inference calls to maximize throughput.

        :param model_name: The name of the model to use for inference.
        :type model_name: str
        :param inputs: A dictionary mapping input names to their
            corresponding data. The data can be either a single numpy array
            (for stacked inputs) or a list of numpy arrays
            (for scatter inputs). All inputs must contain the batch
            dimension, expected shape is (N, ...).
        :type inputs: Dict[str, Union[np.ndarray, List[np.ndarray]]]
        :return: A dictionary mapping output names to their corresponding
            data.
        :rtype: Dict[str, np.ndarray]
        """
        if model_name not in self.registered_models:
            raise ValueError(
                f"Model {model_name} is not registered. "
                "Call register_model first."
            )

        triton_kwargs = {
            "model_version": model_version,
            "request_id": request_id,
            "sequence_id": sequence_id,
            "sequence_start": sequence_start,
            "sequence_end": sequence_end,
            "priority": priority,
            "timeout": timeout,
            "client_timeout": client_timeout,
            "headers": headers,
            "compression_algorithm": compression_algorithm,
            "parameters": parameters,
        }

        ctx = self.registered_models[model_name]

        # 1. Validation & setup
        input_names = list(inputs.keys())
        # We allow inputs[name] to be a list or array, both support len
        lengths = [len(inputs[name]) for name in input_names]
        if len(set(lengths)) != 1:
            raise ValueError(
                f"Input length mismatch. "
                "All inputs must have same sample count. "
                f"Got lengths: {dict(zip(input_names, lengths))}"
            )

        total_samples = lengths[0]
        if total_samples == 0:
            return {}

        # Pre-allocate final output buffers
        # this removes need for np.concatenate later and removes allocation
        # from the callback
        final_results = {}
        for out_name, full_shape, dtype in ctx.output_specs:
            # full shape is (max_batch, ...). We need (total_samples, ...)
            item_shape = full_shape[1:]
            final_results[out_name] = np.empty(
                (total_samples, *item_shape), dtype=dtype
            )

        num_batches = (
            total_samples + ctx.max_batch_size - 1
        ) // ctx.max_batch_size

        # Synchronization
        completion_event = threading.Event()
        # Using a list for mutable int to count completed batches
        state = {"completed": 0, "error": None}

        def callback(
            slot: SHMSlot,
            global_start_idx: int,
            actual_batch_size: int,
            result: grpcclient.InferResult,
            error: grpcclient.InferenceServerException | None,
        ):
            try:
                if error:
                    state["error"] = error
                    # Wake up main thread to throw error
                    completion_event.set()
                    return

                # Direct write to final buffer
                # We write directly from SHM (slot.output_maps) to the
                # pre-allocated final_results; global_start_idx tells use
                # where in the final array this batch belongs.
                global_end_idx = global_start_idx + actual_batch_size

                for out_name, _, _ in ctx.output_specs:
                    # np.copyto is slightly faster than [:] assignment for
                    # large arrays as it bypasses some python overhead, but
                    # slice assignment is also fine.
                    # This performs the COPY from SHM -> Heap (final array)
                    final_results[out_name][
                        global_start_idx:global_end_idx
                    ] = slot.output_maps[out_name][:actual_batch_size]
            except Exception as e:
                state["error"] = e
                completion_event.set()
            finally:
                # Always release the slot back to pool
                ctx.pool.put(slot)

                # Check completion
                state["completed"] += 1
                if state["completed"] == num_batches:
                    completion_event.set()

        # 2. Dispatch loop
        for i in range(num_batches):
            if state["error"]:
                break  # Stop dispatching if error occurred

            start_idx = i * ctx.max_batch_size
            end_idx = min(start_idx + ctx.max_batch_size, total_samples)
            current_bs = end_idx - start_idx

            # Acquire slot (blocks if pool is empty)
            slot = ctx.pool.get()

            try:
                # Write inputs to SHM (zero-copy from python perspective,
                # effectively just a memcpy)
                for name in input_names:
                    # SHM_View[:bs] = User_Heap_View[start:end]
                    user_data_container = inputs[name]
                    target_shm_view = slot.input_maps[name]

                    # Strategy A: Block write (input is stacked array)
                    # Use this if user provides np.array shape (N, ...)
                    if isinstance(user_data_container, np.ndarray):
                        target_shm_view[:current_bs] = user_data_container[
                            start_idx:end_idx
                        ]

                    # Strategy B: Scatter write (input is list of arrays)
                    # Use this strategy if user provides [img1, img2, ...]
                    elif isinstance(user_data_container, list):
                        # get the slice of the list in this batch
                        batch_list = user_data_container[start_idx:end_idx]

                        # Write item by item
                        # This is much faster than
                        # np.stack(batch_list) + memcpy
                        for batch_i, item in enumerate(batch_list):
                            target_shm_view[batch_i] = item
                    else:
                        raise TypeError(
                            f"Input '{name}' must be a np.ndarray or "
                            "List[np.ndarray]. "
                            f"Got {type(user_data_container)}"
                        )

                # Prepare triton handles
                triton_inputs: List[grpcclient.InferInput] = []
                triton_outputs: List[grpcclient.InferRequestedOutput] = []

                # configure input handles
                for name, max_bytes, offset in slot.input_meta:
                    np_array = slot.input_maps[name]

                    # 1. get raw item size (e.g. float32 = 4 bytes)
                    item_size = np_array.itemsize

                    # 2. calculate items per single sample
                    # (excluding batch dim)
                    # shape is (max_batch, H, W, ...) so we slice [1:]
                    sample_size = np.prod(np_array.shape[1:])

                    # 3. calculate exact bytes for this specific batch
                    current_byte_size = int(
                        current_bs * sample_size * item_size
                    )

                    # 4. create infer input with specific batch shape
                    orig_shape = np_array.shape[1:]
                    inp_obj = grpcclient.InferInput(
                        name,
                        [current_bs, *orig_shape],
                        np_to_triton_dtype(np_array.dtype),
                    )

                    # 5. set shm with the calculated size, not the max size
                    inp_obj.set_shared_memory(
                        region_name=slot.region_name,
                        byte_size=current_byte_size,
                        offset=offset,
                    )
                    triton_inputs.append(inp_obj)

                # configure output handles
                for name, max_bytes, offset in slot.output_meta:
                    np_array = slot.output_maps[name]

                    item_size = np_array.itemsize
                    sample_size = np.prod(np_array.shape[1:])
                    current_byte_size = int(
                        current_bs * sample_size * item_size
                    )

                    out_obj = grpcclient.InferRequestedOutput(name)

                    # Strictly limit the output buffer Triton is allowed to
                    # write to.
                    # This prevents Triton from trying to write 8 items into
                    # a request that only has 4 inputs.
                    out_obj.set_shared_memory(
                        region_name=slot.region_name,
                        byte_size=current_byte_size,
                        offset=offset,
                    )
                    triton_outputs.append(out_obj)

                # Async infer
                self.async_infer(
                    model_name=model_name,
                    inputs=triton_inputs,
                    callback=partial(callback, slot, start_idx, current_bs),
                    outputs=triton_outputs,
                    **triton_kwargs,
                )
            except Exception as e:
                ctx.pool.put(slot)  # release slot on error
                raise e

        # 4. Wait for completion
        completion_event.wait()

        if state["error"]:
            raise RuntimeError(f"Inference callback error: {state['error']}")

        return final_results

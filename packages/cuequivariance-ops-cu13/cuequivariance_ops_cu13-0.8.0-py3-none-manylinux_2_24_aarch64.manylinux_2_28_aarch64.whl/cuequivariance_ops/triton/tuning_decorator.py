# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import inspect
import logging  # Added logging import
from typing import Any, Callable

from tqdm import tqdm

from .cache_manager import get_cache_manager

# Configure logging
logger = logging.getLogger(__name__)


def input_to_key_default(**args) -> str:
    key_parts = []
    for arg in args:
        if hasattr(arg, "shape") and hasattr(arg, "dtype"):
            key_parts.append(f"{list(arg.shape)}_{arg.dtype}")
        elif isinstance(arg, bool):
            key_parts.append("True" if arg else "False")
        elif isinstance(arg, str):
            key_parts.append(arg)
        else:
            key_parts.append(str(arg.__class__.__name__))

    return "_".join(key_parts)


def combine_all_kwargs(
    fn: Callable,
    args: tuple,
    kwargs: dict[str, Any],
) -> dict[str, Any]:
    # Get the function signature
    sig = inspect.signature(fn)
    params = sig.parameters
    param_names = list(params.keys())

    # Create dictionary of default values
    defaults = {
        name: param.default
        for name, param in params.items()
        if param.default is not inspect.Parameter.empty
    }
    # Create dictionary mapping positional args to parameter names
    args_as_kwargs = {
        param_names[i]: args[i] for i in range(min(len(args), len(param_names)))
    }
    # Create combined dictionary of all parameters
    all_kwargs = defaults.copy()  # Start with defaults
    all_kwargs.update(args_as_kwargs)  # Override with positional args
    all_kwargs.update(kwargs)  # Override with explicit kwargs

    return all_kwargs


def autotune_aot(
    input_generator: Callable,
    input_to_key: Callable | None,
    input_configs: list[dict[str, Any]],
    tunable_configs: list[dict[str, Any]],
    prune_configs_fn: Callable[
        [list[dict[str, Any]], dict[str, Any]], list[dict[str, Any]]
    ]
    | None,
    run_decoy: Callable[[Callable, dict[str, Any]], None],
    run_bench: Callable[[Callable, dict[str, Any]], float],
) -> None:
    def decorator(fn: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            all_kwargs = combine_all_kwargs(fn, args, kwargs)
            nonlocal input_to_key
            nonlocal input_configs

            if input_to_key is None:
                input_to_key = input_to_key_default

            # Check if the function is already cached
            function_key = fn.__name__
            input_key = input_to_key(**all_kwargs)
            cache_manager = get_cache_manager()
            best_cached_config = cache_manager.get(function_key, input_key)

            aot_mode = cache_manager.aot_mode

            if best_cached_config is None and aot_mode is not None:
                # start autotuning process
                # input_configs = input_configs + [None]
                if aot_mode == "ONDEMAND":
                    input_configs = [None]

                try:
                    # Initialize the progress bar
                    progress_bar = tqdm(
                        input_configs, desc="Autotuning Progress", unit="config"
                    )

                    for input_config in progress_bar:
                        # generate input based on the config
                        input_data = (
                            input_generator(**input_config)
                            if input_config is not None
                            else all_kwargs
                        )

                        # Make a copy of all_kwargs to avoid modifying the original
                        current_kwargs = all_kwargs.copy()
                        current_kwargs.update(input_data)
                        current_input_key = input_to_key(**current_kwargs)

                        best_cached_config = cache_manager.get(
                            function_key, current_input_key
                        )

                        if best_cached_config is not None:
                            continue

                        # prune the tunable configs based on the all_kwargs
                        pruned_tunable_configs = (
                            prune_configs_fn(tunable_configs, **all_kwargs)
                            if prune_configs_fn is not None
                            else tunable_configs
                        )

                        best_config = None
                        best_time = float("inf")
                        working_config = []
                        for tunable in pruned_tunable_configs:
                            try:
                                current_kwargs.update(tunable)
                                run_decoy(fn, current_kwargs)
                                working_config.append(tunable)
                            except Exception:
                                pass

                        if not working_config:
                            logger.warning(
                                f"No valid configurations found for input: {current_input_key}"
                            )
                            continue

                        for tunable in working_config:
                            current_kwargs.update(tunable)
                            elapse = run_bench(fn, current_kwargs)
                            if elapse < best_time:
                                best_time = elapse
                                best_config = tunable

                        cache_manager.set(
                            function_key,
                            current_input_key,
                            {"config": best_config, "time": best_time},
                        )
                    cache_manager.save_cache(function_key)
                except Exception as e:
                    print(f"Stopping autotuning due to error: {e}")

                # After tuning, try to get the best config
                best_cached_config = cache_manager.get(function_key, input_key)

            if best_cached_config is not None:
                all_kwargs.update(best_cached_config["config"])

            return fn(**all_kwargs)

        return wrapper

    return decorator

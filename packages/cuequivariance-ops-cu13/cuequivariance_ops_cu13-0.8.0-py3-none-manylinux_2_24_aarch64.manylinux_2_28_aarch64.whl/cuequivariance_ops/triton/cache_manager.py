# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import hashlib
import json
import logging
import math
import os
from multiprocessing import Lock
from pathlib import Path
from typing import Any

import pynvml
from platformdirs import user_cache_dir

# Configure logging
logger = logging.getLogger(__name__)

FILE_LOCK = Lock()


def get_triton_tuning_mode():
    cueq_at = os.getenv("CUEQ_TRITON_TUNING")
    if cueq_at is not None and cueq_at not in ["AOT", "ONDEMAND"]:
        logger.error(f"CUEQ_TRITON_TUNING setting not recognized: {cueq_at}.\n")
    return cueq_at


def is_docker():
    cgroup = Path("/proc/self/cgroup")
    return Path("/.dockerenv").is_file() or (
        cgroup.is_file() and "docker" in cgroup.read_text()
    )


def overridden_cache_dir():
    return os.getenv("CUEQ_TRITON_CACHE_DIR")


def get_triton_cache_dir() -> Path:
    cache_dir = overridden_cache_dir()
    if cache_dir is None:
        cache_dir = user_cache_dir(appname="cuequivariance-triton", ensure_exists=False)
    cache_dir = Path(cache_dir)
    if cache_dir.exists():
        return cache_dir
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_gpu_information():
    # Default values (NVIDIA RTX A6000 specs)
    defaults = {
        "name": "NVIDIA RTX A6000",
        "major": 8,
        "minor": 6,
        "total_memory": 45,
        "multi_processor_count": 84,
        "power_limit": 300,
        "clock_rate": 2100,
    }

    try:
        pynvml.nvmlInit()
        # Note: non-uniform multi-GPU setups are not supported
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        name = pynvml.nvmlDeviceGetName(handle)
        # pci_info = pynvml.nvmlDeviceGetPciInfo(handle)
        # device_id = pci_info.pciDeviceId
        # sub_device_id = pci_info.pciSubSystemId
        power_limit = pynvml.nvmlDeviceGetPowerManagementLimit(handle)
        max_clock_rate = pynvml.nvmlDeviceGetMaxClockInfo(
            handle, pynvml.NVML_CLOCK_GRAPHICS
        )
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        gpu_core_count = pynvml.nvmlDeviceGetNumGpuCores(handle)
        major, minor = pynvml.nvmlDeviceGetCudaComputeCapability(handle)

        total_memory = math.ceil(mem_info.total / (1024**3))
        multi_processor_count = gpu_core_count // 128
        power_limit_kw = power_limit // 1000

        # Validate all values - if any are invalid, raise exception to use defaults
        if not name or not isinstance(name, str):
            raise ValueError("Invalid GPU name")
        if not isinstance(major, int) or major <= 0:
            raise ValueError("Invalid compute capability major version")
        if not isinstance(minor, int) or minor < 0:
            raise ValueError("Invalid compute capability minor version")
        if not isinstance(total_memory, int) or total_memory <= 0:
            raise ValueError("Invalid total memory")
        if not isinstance(multi_processor_count, int) or multi_processor_count <= 0:
            raise ValueError("Invalid multi-processor count")
        if not isinstance(power_limit_kw, int) or power_limit_kw <= 0:
            raise ValueError("Invalid power limit")
        if not isinstance(max_clock_rate, int) or max_clock_rate <= 0:
            raise ValueError("Invalid clock rate")

        logger.debug(
            f"GPU information: {name}, {major}, {minor}, {total_memory}, {multi_processor_count}, {power_limit_kw}, {max_clock_rate}"
        )
        return {
            "name": name,
            # "device_id": device_id,
            # "sub_device_id": sub_device_id,
            "total_memory": total_memory,
            "multi_processor_count": multi_processor_count,
            "power_limit": power_limit_kw,
            "clock_rate": max_clock_rate,
            "major": major,
            "minor": minor,
        }
    except Exception as e:
        logger.warning(
            f"Failed to get GPU information from pynvml: {e}. Using default values."
        )
        print(
            f"GPU information: {defaults['name']}, {defaults['major']}, {defaults['minor']}, {defaults['total_memory']}, {defaults['multi_processor_count']}, {defaults['power_limit']}, {defaults['clock_rate']}"
        )
        return defaults
    finally:
        try:
            pynvml.nvmlShutdown()
        except Exception:
            pass


def gpu_information_to_key(information: dict) -> str:
    information.pop("name", None)
    key_string = "_".join(f"{value}" for value in information.values()).replace(
        " ", "_"
    )
    hash_object = hashlib.sha256(key_string.encode())
    hash_str = hash_object.hexdigest()
    return hash_str


def load_json(json_file):
    with FILE_LOCK:
        with open(json_file, "rb") as f:
            fn_cache = json.load(f)
    return fn_cache


class CacheManager:
    """Singleton managing the cache"""

    def __init__(self):
        self.gpu_cache = {}
        self.gpu_information = get_gpu_information()
        self.gpu_key = gpu_information_to_key(self.gpu_information)
        self.site_json_path = str(os.path.join(os.path.dirname(__file__), "cache"))
        self.json_path = str(get_triton_cache_dir())
        self.dirty = {}

        if os.getenv("CUEQ_TRITON_IGNORE_EXISTING_CACHE") == "1":
            logger.warning(
                f"\n!!!!!! CUEQ_TRITON_IGNORE_EXISTING_CACHE is ON - previously saved setting will be ignored !!!!!!\n"
                f"CUEQ_TRITON_TUNING is set to {self.aot_mode}\n"
                f"The tuning changes will be written to {self.json_path}"
            )

        if (
            self.aot_mode is not None
            and is_docker()
            and os.getenv("HOME") == "/root"
            and not overridden_cache_dir()
        ):
            logger.warning(
                f"\n!!!!!! CUEQ_TRITON_TUNING is set to {self.aot_mode} and you are running as root in a Docker container. !!!!!!\n"
                f"The tuning changes will be written to {self.json_path}"
                "\nPlease remember to commit the container - otherwise any tuning changes will be lost on container restart."
            )

    # define aot_mode as a property to allow the environment variable to change during runtime
    @property
    def aot_mode(self):
        return get_triton_tuning_mode()

    def load_cache(self, fn_key: str) -> dict:
        # load the json file and store it in the cache-dict
        # if the file does not exist, create an empty dict for the specified function
        fn_cache = {}
        gpu_cache = {}
        best_key = None

        major, minor = self.gpu_information["major"], self.gpu_information["minor"]
        basename = f"{fn_key}.{major}.{minor}.json"
        json_file = f"{self.json_path}/{basename}"

        def result(self, gpu_cache):
            # empty cache or fuzzy match, update for possible save
            if best_key or not gpu_cache:
                gpu_cache["gpu_information"] = self.gpu_information
            self.gpu_cache[fn_key] = gpu_cache
            return gpu_cache

        if os.getenv("CUEQ_TRITON_IGNORE_EXISTING_CACHE"):
            return result(self, gpu_cache)

        try:
            fn_cache = load_json(json_file)

        except Exception as e0:
            site_json_file = f"{self.site_json_path}/{basename}"
            try:
                fn_cache = load_json(site_json_file)
            except Exception as e:
                logger.warning(
                    f"Error reading system-wide triton tuning cache file: {site_json_file}\n{e}\n"
                    f"Error reading users triton tuning cache file {json_file}:\n{e0}"
                )
                pass
        if fn_cache:
            gpu_cache = fn_cache.get(self.gpu_key)
            if gpu_cache is None:
                # do a fuzzy match of config:
                def within_10_percent(a, b, key):
                    a = int(a[key])
                    b = int(b[key])
                    return abs(a - b) / (a + b) < 0.2

                def full_match(a, b):
                    # matching clock & memory
                    return (
                        a["total_memory"] == b["total_memory"]
                        and a["clock_rate"] == b["clock_rate"]
                    )

                def partial_match(a, b):
                    # matching clk or memory whichever matches
                    return within_10_percent(a, b, "total_memory") or within_10_percent(
                        a, b, "clock_rate"
                    )

                for key in fn_cache:
                    conf = fn_cache[key].get("gpu_information")
                    if conf:
                        if full_match(conf, self.gpu_information):
                            best_key = key
                            break
                        elif partial_match(conf, self.gpu_information):
                            best_key = key
                if best_key is None:
                    # just pick the first entry there
                    best_key = next(iter(fn_cache))
                gpu_cache = fn_cache[best_key]

        return result(self, gpu_cache)

    def save_cache(self, fn_key: str) -> None:
        # save cache-dict to json file
        major, minor = self.gpu_information["major"], self.gpu_information["minor"]
        basename = f"{fn_key}.{major}.{minor}.json"
        json_file = os.path.join(self.json_path, basename)

        # Load existing data from the file if it exists
        if os.path.exists(json_file):
            with FILE_LOCK, open(json_file, "rb") as f:
                existing_data = json.load(f)
        else:
            existing_data = {}
        # Update the entry for our GPU key with our data
        existing_data.setdefault(self.gpu_key, {}).update(self.gpu_cache[fn_key])
        self.gpu_cache[fn_key] = existing_data[self.gpu_key]
        merged_data = existing_data
        temp_file = f"{json_file}.{os.getpid()}.tmp"
        try:
            # Save the merged data back to the file
            with FILE_LOCK:
                with open(temp_file, "w") as f:
                    json.dump(merged_data, f, indent=4)
                os.replace(temp_file, json_file)
        except Exception as e:
            logger.warning(f"Warning: Failed to write autotune cache: {e}")

        # Clear the dirty flag
        del self.dirty[fn_key]

    def get(self, fn_key: str, inp_key: str) -> Any:
        # get value from cache
        # if necessary, load json first
        gpu_cache = self.gpu_cache.get(fn_key)
        if gpu_cache is None:
            gpu_cache = self.load_cache(fn_key)
        # check if fn_key and inp_key exist in cache
        return gpu_cache.get(inp_key)

    def set(self, fn_key: str, inp_key: str, value: Any) -> None:
        # write value to cache-dict
        self.gpu_cache[fn_key][inp_key] = value
        self.dirty[fn_key] = 1


cache_manager = CacheManager()


def get_cache_manager():
    return cache_manager

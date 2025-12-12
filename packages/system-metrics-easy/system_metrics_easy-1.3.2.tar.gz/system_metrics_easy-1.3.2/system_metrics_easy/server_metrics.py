#!/usr/bin/env python3

import json
import os
import re
import subprocess
import time
import platform
import signal
import sys
import argparse
import socketio
import io
import csv
from contextlib import contextmanager
from typing import Dict, List, Optional, Union, Any
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


__version__ = "1.3.1"

TIME_INTERVAL = int(os.getenv("TIME_INTERVAL") or "10")
# SOCKET_SERVER_URL = "http://localhost:8000"
SOCKET_SERVER_URL = "https://api.server-metrics.letz.chat"  # Hardcoded backend URL
SERVER_ID = os.getenv("SERVER_ID") or f"server-{platform.node()}"


class ServerMetrics:
    def __init__(self):
        self.previous_net_stats = None
        self.previous_time = None
        self.previous_cpu_times = None
        self.max_retries = 3
        self.timeout_seconds = 10
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""

        def signal_handler(signum, frame):
            print(f"Received signal {signum}, shutting down gracefully...")
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    @contextmanager
    def safe_subprocess(self, cmd: List[str], timeout: int = None):
        """Context manager for safe subprocess execution"""
        process = None
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=None if os.name == "nt" else os.setsid,
            )
            yield process
        except FileNotFoundError:
            # FileNotFoundError is expected when tools don't exist
            # Let the caller handle it with appropriate messages
            raise
        except Exception as e:
            print(f"Subprocess error: {e}")
            raise
        finally:
            if process:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except (subprocess.TimeoutExpired, ProcessLookupError):
                    try:
                        process.kill()
                    except ProcessLookupError:
                        pass

    def _safe_float(self, value: Any, default: float = 0.0) -> float:
        """Safely convert value to float with default fallback"""
        try:
            return float(value) if value is not None else default
        except (ValueError, TypeError):
            return default

    def _safe_int(self, value: Any, default: int = 0) -> int:
        """Safely convert value to int with default fallback"""
        try:
            return int(value) if value is not None else default
        except (ValueError, TypeError):
            return default

    def _validate_positive_number(
        self, value: Union[int, float], name: str
    ) -> Union[int, float]:
        """Validate that a number is positive"""
        if value < 0:
            print(f"Warning: {name} is negative ({value}), setting to 0")
            return 0
        return value

    def get_cpu_usage(self) -> Dict[str, Any]:
        """Get CPU usage per core and total with robust error handling"""
        try:
            import psutil

            # Validate psutil is working
            if not hasattr(psutil, "cpu_percent"):
                raise ImportError("psutil version too old or corrupted")

            # Get per-core CPU usage with consistent interval and retry logic
            per_cpu = None
            total_cpu = None

            for attempt in range(self.max_retries):
                try:
                    # Method 1: Try the standard psutil approach with proper initialization
                    if self.previous_cpu_times is None:
                        # First run - initialize
                        psutil.cpu_percent(interval=None, percpu=True)
                        time.sleep(0.1)
                        per_cpu = psutil.cpu_percent(interval=None, percpu=True)
                        self.previous_cpu_times = time.time()
                    else:
                        # Subsequent runs - use interval for better accuracy
                        per_cpu = psutil.cpu_percent(interval=0.1, percpu=True)

                    # Calculate total CPU from per-core data
                    if per_cpu and len(per_cpu) > 0:
                        total_cpu = sum(per_cpu) / len(per_cpu)
                    else:
                        # Fallback: get total CPU directly
                        if self.previous_cpu_times is None:
                            psutil.cpu_percent(interval=None)
                            time.sleep(0.1)
                        total_cpu = psutil.cpu_percent(interval=0.1)

                    # Validate the data
                    if per_cpu is None:
                        raise ValueError("Per-core CPU data is None")

                    # Check for reasonable values
                    if not isinstance(per_cpu, (list, tuple)) or len(per_cpu) == 0:
                        raise ValueError("Invalid per-core CPU data")

                    if (
                        not isinstance(total_cpu, (int, float))
                        or total_cpu < 0
                        or total_cpu > 1000
                    ):
                        raise ValueError(f"Invalid total CPU value: {total_cpu}")

                    # Update previous time for next call
                    self.previous_cpu_times = time.time()

                    break

                except Exception as e:
                    if attempt == self.max_retries - 1:
                        raise e
                    print(f"Warning: CPU metrics attempt {attempt + 1} failed: {e}")
                    time.sleep(0.2)

            # Get load average safely
            load_avg = None
            try:
                if hasattr(os, "getloadavg"):
                    load_avg = os.getloadavg()
                    if load_avg and len(load_avg) >= 3:
                        load_avg = [
                            self._validate_positive_number(la, f"load_avg[{i}]")
                            for i, la in enumerate(load_avg)
                        ]
                    else:
                        load_avg = None
            except (OSError, AttributeError) as e:
                print(f"Warning: Load average not available: {e}")

            # Validate and clean per-core data
            safe_per_cpu = []
            for i, cpu in enumerate(per_cpu):
                safe_cpu = self._safe_float(cpu, 0.0)
                safe_cpu = self._validate_positive_number(safe_cpu, f"CPU core {i}")
                safe_cpu = min(safe_cpu, 100.0)  # Cap at 100%
                safe_per_cpu.append(round(safe_cpu, 2))

            # Validate total CPU
            safe_total_cpu = self._safe_float(total_cpu, 0.0)
            safe_total_cpu = self._validate_positive_number(safe_total_cpu, "total CPU")
            safe_total_cpu = min(safe_total_cpu, 100.0)  # Cap at 100%

            return {
                "total": round(safe_total_cpu, 2),
                "per_core": safe_per_cpu,
                "core_count": len(safe_per_cpu),
                "load_average": {
                    "1min": round(load_avg[0], 2)
                    if load_avg and len(load_avg) > 0
                    else None,
                    "5min": round(load_avg[1], 2)
                    if load_avg and len(load_avg) > 1
                    else None,
                    "15min": round(load_avg[2], 2)
                    if load_avg and len(load_avg) > 2
                    else None,
                },
            }
        except ImportError as e:
            print(f"Error: psutil import failed: {e}")
            return {
                "error": "psutil module not available. Install with: pip install psutil"
            }
        except Exception as e:
            print(f"Error: CPU metrics error: {e}")
            return {"error": f"CPU metrics not available: {str(e)}"}

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get RAM usage statistics with robust error handling"""
        try:
            import psutil

            # Validate psutil is working
            if not hasattr(psutil, "virtual_memory"):
                raise ImportError("psutil version too old or corrupted")

            # Get memory info with retry logic
            memory = None
            swap = None

            for attempt in range(self.max_retries):
                try:
                    memory = psutil.virtual_memory()
                    swap = psutil.swap_memory()

                    # Validate memory data
                    if not hasattr(memory, "total") or memory.total <= 0:
                        raise ValueError("Invalid memory total")

                    if not hasattr(memory, "used") or memory.used < 0:
                        raise ValueError("Invalid memory used")

                    if not hasattr(memory, "free") or memory.free < 0:
                        raise ValueError("Invalid memory free")

                    if not hasattr(memory, "available") or memory.available < 0:
                        raise ValueError("Invalid memory available")

                    # Validate swap data
                    if not hasattr(swap, "total") or swap.total < 0:
                        raise ValueError("Invalid swap total")

                    if not hasattr(swap, "used") or swap.used < 0:
                        raise ValueError("Invalid swap used")

                    break

                except Exception as e:
                    if attempt == self.max_retries - 1:
                        raise e
                    print(f"Warning: Memory metrics attempt {attempt + 1} failed: {e}")
                    time.sleep(0.1)

            # Convert to GB with validation
            total_gb = self._safe_float(memory.total / (1024**3), 0.0)
            used_gb = self._safe_float(memory.used / (1024**3), 0.0)
            free_gb = self._safe_float(memory.free / (1024**3), 0.0)
            available_gb = self._safe_float(memory.available / (1024**3), 0.0)

            # Validate memory values
            total_gb = self._validate_positive_number(total_gb, "memory total")
            used_gb = self._validate_positive_number(used_gb, "memory used")
            free_gb = self._validate_positive_number(free_gb, "memory free")
            available_gb = self._validate_positive_number(
                available_gb, "memory available"
            )

            # Ensure used doesn't exceed total
            if used_gb > total_gb:
                print(
                    f"Warning: Memory used ({used_gb} GB) exceeds total ({total_gb} GB)"
                )
                used_gb = total_gb

            # Calculate percentage safely
            used_percent = 0.0
            if total_gb > 0:
                used_percent = (used_gb / total_gb) * 100
                used_percent = min(used_percent, 100.0)  # Cap at 100%

            # Swap calculations
            swap_total_gb = self._safe_float(swap.total / (1024**3), 0.0)
            swap_used_gb = self._safe_float(swap.used / (1024**3), 0.0)

            swap_total_gb = self._validate_positive_number(swap_total_gb, "swap total")
            swap_used_gb = self._validate_positive_number(swap_used_gb, "swap used")

            # Ensure swap used doesn't exceed swap total
            if swap_used_gb > swap_total_gb:
                print(
                    f"Warning: Swap used ({swap_used_gb} GB) exceeds swap total ({swap_total_gb} GB)"
                )
                swap_used_gb = swap_total_gb

            # Calculate swap percentage safely
            swap_percent = 0.0
            if swap_total_gb > 0:
                swap_percent = (swap_used_gb / swap_total_gb) * 100
                swap_percent = min(swap_percent, 100.0)  # Cap at 100%
            else:
                swap_percent = self._safe_float(swap.percent, 0.0)
                swap_percent = min(swap_percent, 100.0)

            return {
                "total_gb": round(total_gb, 2),
                "used_gb": round(used_gb, 2),
                "free_gb": round(free_gb, 2),
                "available_gb": round(available_gb, 2),
                "used_percent": round(used_percent, 2),
                "swap_total_gb": round(swap_total_gb, 2),
                "swap_used_gb": round(swap_used_gb, 2),
                "swap_percent": round(swap_percent, 2),
            }
        except ImportError as e:
            print(f"Error: psutil import failed: {e}")
            return {
                "error": "psutil module not available. Install with: pip install psutil"
            }
        except Exception as e:
            print(f"Error: Memory metrics error: {e}")
            return {"error": f"Memory metrics not available: {str(e)}"}

    def get_disk_usage(self) -> Union[List[Dict[str, Any]], Dict[str, str]]:
        """Get disk usage for all mounted filesystems with robust error handling"""
        try:
            import psutil

            # Validate psutil is working
            if not hasattr(psutil, "disk_partitions"):
                raise ImportError("psutil version too old or corrupted")

            disk_info = []
            partitions = None

            # Get partitions with retry logic
            for attempt in range(self.max_retries):
                try:
                    partitions = psutil.disk_partitions()
                    if not isinstance(partitions, (list, tuple)):
                        raise ValueError("Invalid partitions data")
                    break
                except Exception as e:
                    if attempt == self.max_retries - 1:
                        raise e
                    print(f"Warning: Disk partitions attempt {attempt + 1} failed: {e}")
                    time.sleep(0.1)

            # Process each partition safely
            for partition in partitions:
                try:
                    # Validate partition data
                    if not hasattr(partition, "device") or not hasattr(
                        partition, "mountpoint"
                    ):
                        print("Warning: Invalid partition data, skipping")
                        continue

                    # Skip problematic mount points
                    mountpoint = partition.mountpoint
                    if not mountpoint or mountpoint in ["", "/proc", "/sys", "/dev"]:
                        continue

                    # Get disk usage with timeout protection
                    usage = None
                    for attempt in range(self.max_retries):
                        try:
                            usage = psutil.disk_usage(mountpoint)

                            # Validate usage data
                            if not hasattr(usage, "total") or usage.total <= 0:
                                raise ValueError("Invalid disk total")

                            if not hasattr(usage, "used") or usage.used < 0:
                                raise ValueError("Invalid disk used")

                            if not hasattr(usage, "free") or usage.free < 0:
                                raise ValueError("Invalid disk free")

                            break

                        except (PermissionError, OSError, FileNotFoundError) as e:
                            print(f"Debug: Cannot access {mountpoint}: {e}")
                            break
                        except Exception as e:
                            if attempt == self.max_retries - 1:
                                print(
                                    f"Warning: Disk usage for {mountpoint} failed: {e}"
                                )
                                break
                            time.sleep(0.1)

                    if usage is None:
                        continue

                    # Convert to GB with validation
                    total_gb = self._safe_float(usage.total / (1024**3), 0.0)
                    used_gb = self._safe_float(usage.used / (1024**3), 0.0)
                    free_gb = self._safe_float(usage.free / (1024**3), 0.0)

                    # Validate values
                    total_gb = self._validate_positive_number(
                        total_gb, f"disk total for {mountpoint}"
                    )
                    used_gb = self._validate_positive_number(
                        used_gb, f"disk used for {mountpoint}"
                    )
                    free_gb = self._validate_positive_number(
                        free_gb, f"disk free for {mountpoint}"
                    )

                    # Ensure used doesn't exceed total
                    if used_gb > total_gb:
                        print(
                            f"Warning: Disk used ({used_gb} GB) exceeds total ({total_gb} GB) for {mountpoint}"
                        )
                        used_gb = total_gb

                    # Calculate percentage safely
                    used_percent = 0.0
                    if total_gb > 0:
                        used_percent = (used_gb / total_gb) * 100
                        used_percent = min(used_percent, 100.0)  # Cap at 100%

                    # Sanitize strings
                    device = (
                        str(partition.device)
                        if hasattr(partition, "device")
                        else "Unknown"
                    )
                    fstype = (
                        str(partition.fstype)
                        if hasattr(partition, "fstype")
                        else "Unknown"
                    )

                    disk_info.append(
                        {
                            "device": device,
                            "mountpoint": mountpoint,
                            "fstype": fstype,
                            "total_gb": round(total_gb, 2),
                            "used_gb": round(used_gb, 2),
                            "free_gb": round(free_gb, 2),
                            "used_percent": round(used_percent, 2),
                        }
                    )

                except Exception as e:
                    print(
                        f"Warning: Error processing partition {getattr(partition, 'device', 'Unknown')}: {e}"
                    )
                    continue

            return disk_info if disk_info else []

        except ImportError as e:
            print(f"Error: psutil import failed: {e}")
            return {
                "error": "psutil module not available. Install with: pip install psutil"
            }
        except Exception as e:
            print(f"Error: Disk metrics error: {e}")
            return {"error": f"Disk metrics not available: {str(e)}"}

    def get_network_usage(self) -> Union[List[Dict[str, Any]], Dict[str, str]]:
        """Get network throughput per second with robust error handling"""
        try:
            import psutil

            # Validate psutil is working
            if not hasattr(psutil, "net_io_counters"):
                raise ImportError("psutil version too old or corrupted")

            # Get network stats with retry logic
            current_net_stats = None
            for attempt in range(self.max_retries):
                try:
                    current_net_stats = psutil.net_io_counters(pernic=True)
                    if not isinstance(current_net_stats, dict):
                        raise ValueError("Invalid network stats data")
                    break
                except Exception as e:
                    if attempt == self.max_retries - 1:
                        raise e
                    print(f"Warning: Network stats attempt {attempt + 1} failed: {e}")
                    time.sleep(0.1)

            current_time = time.time()
            network_data = []

            # Handle first run or missing previous data
            if self.previous_net_stats is None or self.previous_time is None:
                self.previous_net_stats = current_net_stats
                self.previous_time = current_time

                for interface, stats in current_net_stats.items():
                    try:
                        # Validate interface name
                        if not interface or not isinstance(interface, str):
                            continue

                        # Validate stats object
                        if not hasattr(stats, "bytes_sent") or not hasattr(
                            stats, "bytes_recv"
                        ):
                            continue

                        bytes_sent = self._safe_int(stats.bytes_sent, 0)
                        bytes_recv = self._safe_int(stats.bytes_recv, 0)

                        bytes_sent = self._validate_positive_number(
                            bytes_sent, f"bytes_sent for {interface}"
                        )
                        bytes_recv = self._validate_positive_number(
                            bytes_recv, f"bytes_recv for {interface}"
                        )

                        network_data.append(
                            {
                                "interface": str(interface),
                                "bytes_sent_per_sec": 0,
                                "bytes_recv_per_sec": 0,
                                "mb_sent_per_sec": 0,
                                "mb_recv_per_sec": 0,
                                "total_sent_gb": round(bytes_sent / (1024**3), 2),
                                "total_recv_gb": round(bytes_recv / (1024**3), 2),
                            }
                        )
                    except Exception as e:
                        print(f"Warning: Error processing interface {interface}: {e}")
                        continue

                return network_data

            # Calculate throughput
            time_delta = current_time - self.previous_time

            # Validate time delta
            if time_delta <= 0 or time_delta > 3600:  # Max 1 hour
                print(f"Warning: Invalid time delta: {time_delta}, resetting")
                self.previous_net_stats = current_net_stats
                self.previous_time = current_time
                return self.get_network_usage()  # Recursive call with reset data

            for interface, stats in current_net_stats.items():
                try:
                    # Validate interface name
                    if not interface or not isinstance(interface, str):
                        continue

                    # Check if interface exists in previous stats
                    if interface not in self.previous_net_stats:
                        continue

                    prev_stats = self.previous_net_stats[interface]

                    # Validate stats objects
                    if not hasattr(stats, "bytes_sent") or not hasattr(
                        stats, "bytes_recv"
                    ):
                        continue
                    if not hasattr(prev_stats, "bytes_sent") or not hasattr(
                        prev_stats, "bytes_recv"
                    ):
                        continue

                    # Get current and previous values safely
                    current_sent = self._safe_int(stats.bytes_sent, 0)
                    current_recv = self._safe_int(stats.bytes_recv, 0)
                    prev_sent = self._safe_int(prev_stats.bytes_sent, 0)
                    prev_recv = self._safe_int(prev_stats.bytes_recv, 0)

                    # Validate values
                    current_sent = self._validate_positive_number(
                        current_sent, f"current bytes_sent for {interface}"
                    )
                    current_recv = self._validate_positive_number(
                        current_recv, f"current bytes_recv for {interface}"
                    )
                    prev_sent = self._validate_positive_number(
                        prev_sent, f"prev bytes_sent for {interface}"
                    )
                    prev_recv = self._validate_positive_number(
                        prev_recv, f"prev bytes_recv for {interface}"
                    )

                    # Calculate differences
                    bytes_sent_diff = current_sent - prev_sent
                    bytes_recv_diff = current_recv - prev_recv

                    # Handle counter wraparound (32-bit or 64-bit)
                    if bytes_sent_diff < 0:
                        # Assume wraparound, calculate max possible value
                        max_32bit = 2**32 - 1
                        max_64bit = 2**64 - 1
                        if prev_sent > max_32bit:
                            bytes_sent_diff = (max_64bit - prev_sent) + current_sent
                        else:
                            bytes_sent_diff = (max_32bit - prev_sent) + current_sent

                    if bytes_recv_diff < 0:
                        if prev_recv > max_32bit:
                            bytes_recv_diff = (max_64bit - prev_recv) + current_recv
                        else:
                            bytes_recv_diff = (max_32bit - prev_recv) + current_recv

                    # Calculate per-second rates
                    bytes_sent_per_sec = bytes_sent_diff / time_delta
                    bytes_recv_per_sec = bytes_recv_diff / time_delta

                    # Cap at reasonable values (1 GB/s)
                    max_rate = 1024**3  # 1 GB/s
                    bytes_sent_per_sec = min(bytes_sent_per_sec, max_rate)
                    bytes_recv_per_sec = min(bytes_recv_per_sec, max_rate)

                    # Ensure non-negative
                    bytes_sent_per_sec = max(0, bytes_sent_per_sec)
                    bytes_recv_per_sec = max(0, bytes_recv_per_sec)

                    network_data.append(
                        {
                            "interface": str(interface),
                            "bytes_sent_per_sec": round(bytes_sent_per_sec, 2),
                            "bytes_recv_per_sec": round(bytes_recv_per_sec, 2),
                            "mb_sent_per_sec": round(bytes_sent_per_sec / (1024**2), 3),
                            "mb_recv_per_sec": round(bytes_recv_per_sec / (1024**2), 3),
                            "total_sent_gb": round(current_sent / (1024**3), 2),
                            "total_recv_gb": round(current_recv / (1024**3), 2),
                        }
                    )

                except Exception as e:
                    print(
                        f"Warning: Error calculating throughput for interface {interface}: {e}"
                    )
                    continue

            # Update previous stats
            self.previous_net_stats = current_net_stats
            self.previous_time = current_time

            return network_data

        except ImportError as e:
            print(f"Error: psutil import failed: {e}")
            return {
                "error": "psutil module not available. Install with: pip install psutil"
            }
        except Exception as e:
            print(f"Error: Network metrics error: {e}")
            return {"error": f"Network metrics not available: {str(e)}"}

    def get_gpu_stats(self) -> Union[List[Dict[str, Any]], Dict[str, str]]:
        """Get GPU statistics for various GPU types (NVIDIA, Apple Silicon, AMD, Intel) with robust error handling"""
        gpu_data = []

        try:
            # Try NVIDIA GPU first
            try:
                nvidia_gpu = self._get_nvidia_gpu_stats()
                if nvidia_gpu and isinstance(nvidia_gpu, list):
                    gpu_data.extend(nvidia_gpu)
            except Exception as e:
                print(f"Debug: NVIDIA GPU detection failed: {e}")

            # Try Apple Silicon GPU (macOS)
            try:
                apple_gpu = self._get_apple_gpu_stats()
                if apple_gpu and isinstance(apple_gpu, list):
                    gpu_data.extend(apple_gpu)
            except Exception as e:
                print(f"Debug: Apple GPU detection failed: {e}")

            # Try AMD GPU
            try:
                amd_gpu = self._get_amd_gpu_stats()
                if amd_gpu and isinstance(amd_gpu, list):
                    gpu_data.extend(amd_gpu)
            except Exception as e:
                print(f"Debug: AMD GPU detection failed: {e}")

            # Try Intel GPU
            try:
                intel_gpu = self._get_intel_gpu_stats()
                if intel_gpu and isinstance(intel_gpu, list):
                    gpu_data.extend(intel_gpu)
            except Exception as e:
                print(f"Debug: Intel GPU detection failed: {e}")

            # Validate and clean GPU data
            validated_gpu_data = []
            for gpu in gpu_data:
                try:
                    if not isinstance(gpu, dict):
                        continue

                    # Ensure required fields exist
                    validated_gpu = {
                        "gpu_id": str(gpu.get("gpu_id", "0")),
                        "name": str(gpu.get("name", "Unknown GPU")),
                        "type": str(gpu.get("type", "Unknown")),
                        "utilization_percent": gpu.get("utilization_percent", "N/A"),
                        "memory_used_mb": gpu.get("memory_used_mb", "N/A"),
                        "memory_total_mb": gpu.get("memory_total_mb", "N/A"),
                        "temperature_c": gpu.get("temperature_c", "N/A"),
                        "memory_used_gb": gpu.get("memory_used_gb", "N/A"),
                        "memory_total_gb": gpu.get("memory_total_gb", "N/A"),
                        "memory_usage_percent": gpu.get("memory_usage_percent", "N/A"),
                    }

                    # Add optional fields if they exist
                    if "note" in gpu:
                        validated_gpu["note"] = str(gpu["note"])

                    validated_gpu_data.append(validated_gpu)

                except Exception as e:
                    print(f"Warning: Error validating GPU data: {e}")
                    continue

            return (
                validated_gpu_data
                if validated_gpu_data
                else {"message": "No GPU detected or GPU monitoring not available"}
            )

        except Exception as e:
            print(f"Error: GPU stats error: {e}")
            return {"error": f"GPU metrics not available: {str(e)}"}

    def _get_nvidia_gpu_stats(self) -> Optional[List[Dict[str, Any]]]:
        """Get NVIDIA GPU statistics using nvidia-smi with robust error handling"""
        # Try JSON format first (most reliable, handles all GPU names including H200)
        try:
            with self.safe_subprocess(
                [
                    "nvidia-smi",
                    "--query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu",
                    "--format=json",
                ],
                timeout=self.timeout_seconds,
            ) as process:
                stdout, stderr = process.communicate(timeout=self.timeout_seconds)

                if process.returncode == 0 and stdout.strip():
                    try:
                        data = json.loads(stdout)
                        # nvidia-smi JSON format: array of GPU objects with flat keys
                        # Handle both array format and object with "gpu" key (for compatibility)
                        if isinstance(data, list):
                            gpu_list = data
                        elif isinstance(data, dict) and "gpu" in data:
                            gpu_list = data.get("gpu", [])
                        else:
                            # Try to find GPU array in nested structure
                            gpu_list = data.get("gpu", [])

                        if gpu_list:
                            gpu_data = []
                            for gpu in gpu_list:
                                try:
                                    # nvidia-smi JSON uses flat keys: "index", "name", "utilization.gpu", etc.
                                    gpu_id = str(gpu.get("index", gpu.get("id", "0")))
                                    name = str(
                                        gpu.get("name", "Unknown NVIDIA GPU")
                                    ).strip()

                                    # Parse utilization - nvidia-smi JSON uses "utilization.gpu" as flat key
                                    utilization_str = (
                                        str(
                                            gpu.get(
                                                "utilization.gpu",
                                                gpu.get("utilization", {}).get(
                                                    "gpu_util", "0"
                                                ),
                                            )
                                        )
                                        .replace("%", "")
                                        .replace(" ", "")
                                        .strip()
                                    )
                                    utilization = self._safe_int(utilization_str, 0)
                                    utilization = self._validate_positive_number(
                                        utilization, f"GPU {gpu_id} utilization"
                                    )
                                    utilization = min(utilization, 100)

                                    # Parse memory used - nvidia-smi JSON uses "memory.used" as flat key
                                    memory_used_str = (
                                        str(
                                            gpu.get(
                                                "memory.used",
                                                gpu.get("fb_memory_usage", {}).get(
                                                    "used", "0"
                                                ),
                                            )
                                        )
                                        .replace("MiB", "")
                                        .replace("MB", "")
                                        .replace(" ", "")
                                        .strip()
                                    )
                                    memory_used_mb = self._safe_int(memory_used_str, 0)
                                    memory_used_mb = self._validate_positive_number(
                                        memory_used_mb, f"GPU {gpu_id} memory used"
                                    )

                                    # Parse memory total - nvidia-smi JSON uses "memory.total" as flat key
                                    memory_total_str = (
                                        str(
                                            gpu.get(
                                                "memory.total",
                                                gpu.get("fb_memory_usage", {}).get(
                                                    "total", "0"
                                                ),
                                            )
                                        )
                                        .replace("MiB", "")
                                        .replace("MB", "")
                                        .replace(" ", "")
                                        .strip()
                                    )
                                    memory_total_mb = self._safe_int(
                                        memory_total_str, 0
                                    )
                                    memory_total_mb = self._validate_positive_number(
                                        memory_total_mb, f"GPU {gpu_id} memory total"
                                    )

                                    # Parse temperature - nvidia-smi JSON uses "temperature.gpu" as flat key
                                    temp_str = (
                                        str(
                                            gpu.get(
                                                "temperature.gpu",
                                                gpu.get("temperature", {}).get(
                                                    "gpu_temp", "0"
                                                ),
                                            )
                                        )
                                        .replace("C", "")
                                        .replace("°", "")
                                        .replace(" ", "")
                                        .strip()
                                    )
                                    temperature = self._safe_int(temp_str, 0)
                                    temperature = self._validate_positive_number(
                                        temperature, f"GPU {gpu_id} temperature"
                                    )
                                    temperature = min(temperature, 200)

                                    # Calculate derived values
                                    memory_used_gb = (
                                        round(memory_used_mb / 1024, 2)
                                        if memory_used_mb > 0
                                        else 0
                                    )
                                    memory_total_gb = (
                                        round(memory_total_mb / 1024, 2)
                                        if memory_total_mb > 0
                                        else 0
                                    )

                                    # Calculate memory usage percentage
                                    memory_usage_percent = 0.0
                                    if memory_total_mb > 0 and memory_used_mb >= 0:
                                        memory_usage_percent = (
                                            memory_used_mb / memory_total_mb
                                        ) * 100
                                        memory_usage_percent = min(
                                            memory_usage_percent, 100.0
                                        )

                                    # Ensure used doesn't exceed total
                                    if (
                                        memory_used_mb > memory_total_mb
                                        and memory_total_mb > 0
                                    ):
                                        print(
                                            f"Warning: GPU {gpu_id} memory used ({memory_used_mb} MB) exceeds total ({memory_total_mb} MB)"
                                        )
                                        memory_used_mb = memory_total_mb
                                        memory_used_gb = memory_total_gb
                                        memory_usage_percent = 100.0

                                    gpu_data.append(
                                        {
                                            "gpu_id": gpu_id,
                                            "name": name,
                                            "type": "NVIDIA",
                                            "utilization_percent": utilization,
                                            "memory_used_mb": memory_used_mb,
                                            "memory_total_mb": memory_total_mb,
                                            "temperature_c": temperature,
                                            "memory_used_gb": memory_used_gb,
                                            "memory_total_gb": memory_total_gb,
                                            "memory_usage_percent": round(
                                                memory_usage_percent, 2
                                            ),
                                        }
                                    )
                                except Exception as e:
                                    print(
                                        f"Warning: Error parsing NVIDIA GPU JSON entry: {e}"
                                    )
                                    continue

                            if gpu_data:
                                return gpu_data
                    except json.JSONDecodeError as e:
                        print(f"Debug: Failed to parse nvidia-smi JSON: {e}")
                        pass  # Fall through to CSV parsing
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass  # Fall through to CSV parsing
        except Exception as e:
            print(f"Debug: nvidia-smi JSON format failed: {e}")

        # Fallback to CSV format with proper CSV parsing (handles commas in GPU names)
        try:
            with self.safe_subprocess(
                [
                    "nvidia-smi",
                    "--query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu",
                    "--format=csv,noheader,nounits",
                ],
                timeout=self.timeout_seconds,
            ) as process:
                stdout, stderr = process.communicate(timeout=self.timeout_seconds)

                if process.returncode != 0:
                    print(
                        f"Debug: nvidia-smi failed with return code {process.returncode}: {stderr}"
                    )
                    return None

                if not stdout.strip():
                    print("Debug: nvidia-smi returned empty output")
                    return None

            gpu_data = []
            # Use Python's csv module for proper parsing (handles quoted fields with commas)
            csv_reader = csv.reader(io.StringIO(stdout.strip()))

            for line_num, parts in enumerate(csv_reader, start=1):
                if not parts or len(parts) < 6:
                    if parts:  # Only warn if there's actual content
                        print(
                            f"Warning: Invalid nvidia-smi output line {line_num}: {','.join(parts)}"
                        )
                    continue

                try:
                    # Parse and validate each field
                    gpu_id = str(parts[0]).strip() if parts[0] else "0"
                    name = str(parts[1]).strip() if parts[1] else "Unknown NVIDIA GPU"

                    # Parse utilization
                    utilization = self._safe_int(parts[2], 0)
                    utilization = self._validate_positive_number(
                        utilization, f"GPU {gpu_id} utilization"
                    )
                    utilization = min(utilization, 100)  # Cap at 100%

                    # Parse memory used
                    memory_used_mb = self._safe_int(parts[3], 0)
                    memory_used_mb = self._validate_positive_number(
                        memory_used_mb, f"GPU {gpu_id} memory used"
                    )

                    # Parse memory total
                    memory_total_mb = self._safe_int(parts[4], 0)
                    memory_total_mb = self._validate_positive_number(
                        memory_total_mb, f"GPU {gpu_id} memory total"
                    )

                    # Parse temperature
                    temperature = self._safe_int(parts[5], 0)
                    temperature = self._validate_positive_number(
                        temperature, f"GPU {gpu_id} temperature"
                    )
                    temperature = min(temperature, 200)  # Cap at 200°C

                    # Calculate derived values safely
                    memory_used_gb = (
                        round(memory_used_mb / 1024, 2) if memory_used_mb > 0 else 0
                    )
                    memory_total_gb = (
                        round(memory_total_mb / 1024, 2) if memory_total_mb > 0 else 0
                    )

                    # Calculate memory usage percentage
                    memory_usage_percent = 0.0
                    if memory_total_mb > 0 and memory_used_mb >= 0:
                        memory_usage_percent = (memory_used_mb / memory_total_mb) * 100
                        memory_usage_percent = min(
                            memory_usage_percent, 100.0
                        )  # Cap at 100%

                    # Ensure used doesn't exceed total
                    if memory_used_mb > memory_total_mb and memory_total_mb > 0:
                        print(
                            f"Warning: GPU {gpu_id} memory used ({memory_used_mb} MB) exceeds total ({memory_total_mb} MB)"
                        )
                        memory_used_mb = memory_total_mb
                        memory_used_gb = memory_total_gb
                        memory_usage_percent = 100.0

                    gpu_data.append(
                        {
                            "gpu_id": gpu_id,
                            "name": name,
                            "type": "NVIDIA",
                            "utilization_percent": utilization,
                            "memory_used_mb": memory_used_mb,
                            "memory_total_mb": memory_total_mb,
                            "temperature_c": temperature,
                            "memory_used_gb": memory_used_gb,
                            "memory_total_gb": memory_total_gb,
                            "memory_usage_percent": round(memory_usage_percent, 2),
                        }
                    )

                except Exception as e:
                    print(f"Warning: Error parsing nvidia-smi line {line_num}: {e}")
                    continue

            return gpu_data if gpu_data else None

        except subprocess.TimeoutExpired:
            print("Warning: nvidia-smi command timed out")
            return None
        except FileNotFoundError:
            print("Debug: nvidia-smi command not found")
            return None
        except Exception as e:
            print(f"Debug: NVIDIA GPU detection failed: {e}")
            return None

    def _get_apple_gpu_stats(self) -> Optional[List[Dict[str, Any]]]:
        """Get Apple Silicon GPU statistics (macOS) with robust error handling"""
        try:
            import platform

            if platform.system() != "Darwin":
                return None

            # Try to get GPU info using system_profiler
            with self.safe_subprocess(
                ["system_profiler", "SPDisplaysDataType", "-json"],
                timeout=self.timeout_seconds,
            ) as process:
                stdout, stderr = process.communicate(timeout=self.timeout_seconds)

                if process.returncode != 0:
                    print(
                        f"Debug: system_profiler failed with return code {process.returncode}: {stderr}"
                    )
                    return None

                if not stdout.strip():
                    print("Debug: system_profiler returned empty output")
                    return None

                try:
                    data = json.loads(stdout)
                except json.JSONDecodeError as e:
                    print(f"Warning: Failed to parse system_profiler JSON: {e}")
                    return None

            gpu_data = []
            displays = data.get("SPDisplaysDataType", [])

            if not isinstance(displays, list):
                print("Debug: Invalid displays data structure")
                return None

            for display in displays:
                try:
                    if not isinstance(display, dict):
                        continue

                    if "sppci_model" not in display:
                        continue

                    gpu_name = str(display["sppci_model"])
                    if not gpu_name or (
                        "Apple" not in gpu_name and "GPU" not in gpu_name
                    ):
                        continue

                    # Get memory info if available
                    memory_info = display.get("spdisplays_vram", "Unknown")
                    memory_mb = 0

                    if isinstance(memory_info, str) and "MB" in memory_info:
                        try:
                            # Extract number from string like "8192 MB"
                            memory_str = memory_info.replace("MB", "").strip()
                            memory_mb = self._safe_int(memory_str, 0)
                            memory_mb = self._validate_positive_number(
                                memory_mb, "Apple GPU memory"
                            )
                        except Exception as e:
                            print(f"Debug: Failed to parse Apple GPU memory: {e}")
                            memory_mb = 0
                    elif isinstance(memory_info, (int, float)):
                        memory_mb = self._safe_int(memory_info, 0)
                        memory_mb = self._validate_positive_number(
                            memory_mb, "Apple GPU memory"
                        )

                    gpu_data.append(
                        {
                            "gpu_id": "0",
                            "name": gpu_name,
                            "type": "Apple Silicon",
                            "utilization_percent": "N/A",  # Not easily available on macOS
                            "memory_used_mb": "N/A",
                            "memory_total_mb": memory_mb,
                            "temperature_c": "N/A",  # Not easily available on macOS
                            "memory_used_gb": "N/A",
                            "memory_total_gb": round(memory_mb / 1024, 2)
                            if memory_mb > 0
                            else "N/A",
                            "memory_usage_percent": "N/A",
                            "note": "Apple Silicon GPU - detailed metrics not available via standard tools",
                        }
                    )

                except Exception as e:
                    print(f"Warning: Error processing Apple GPU display: {e}")
                    continue

            return gpu_data if gpu_data else None

        except subprocess.TimeoutExpired:
            print("Warning: system_profiler command timed out")
            return None
        except FileNotFoundError:
            print("Debug: system_profiler command not found")
            return None
        except Exception as e:
            print(f"Debug: Apple GPU detection failed: {e}")
            return None

    def _get_amd_gpu_stats(self) -> Optional[List[Dict[str, Any]]]:
        """Get AMD GPU statistics using rocm-smi or amd-smi with robust error handling"""
        # Try amd-smi first (newer AMD tool), then fallback to rocm-smi
        for tool_name in ["amd-smi", "rocm-smi"]:
            try:
                # Try with JSON output for easier parsing
                with self.safe_subprocess(
                    [
                        tool_name,
                        "--showid",
                        "--showmeminfo",
                        "vram",
                        "--showuse",
                        "--showtemp",
                        "--json",
                    ],
                    timeout=self.timeout_seconds,
                ) as process:
                    stdout, stderr = process.communicate(timeout=self.timeout_seconds)
                    if process.returncode != 0 or not stdout.strip():
                        continue  # Try next tool

                    try:
                        data = json.loads(stdout)
                        gpu_data = []

                        # Parse JSON output - handle different possible structures
                        # rocm-smi/amd-smi JSON can have different formats
                        if isinstance(data, dict):
                            # Try different possible key structures
                            gpu_dict = data
                            # Some versions use numeric keys, others use string keys
                            if not any(
                                isinstance(k, (int, str)) and "gpu" in str(k).lower()
                                for k in data.keys()
                            ):
                                # Might be nested structure
                                for key in data.keys():
                                    if isinstance(data[key], dict):
                                        gpu_dict = {key: data[key]}
                                        break

                            # Parse each GPU
                            for gpu_id, gpu_info in gpu_dict.items():
                                if not isinstance(gpu_info, dict):
                                    continue

                                try:
                                    # Extract GPU name/ID - try multiple possible keys
                                    name = (
                                        gpu_info.get("Card series")
                                        or gpu_info.get("Card Series")
                                        or gpu_info.get("card_series")
                                        or gpu_info.get("name")
                                        or f"AMD GPU {gpu_id}"
                                    )

                                    # Extract utilization - try multiple possible keys
                                    utilization = 0
                                    for key in [
                                        "GPU use (%)",
                                        "GPU Use (%)",
                                        "gpu_use_percent",
                                        "utilization",
                                    ]:
                                        val = gpu_info.get(key)
                                        if val is not None:
                                            utilization = self._safe_int(val, 0)
                                            break
                                    utilization = min(max(utilization, 0), 100)

                                    # Extract memory info - try multiple possible keys and formats
                                    memory_total_bytes = 0
                                    memory_used_bytes = 0

                                    # Try different key names for total memory
                                    for key in [
                                        "VRAM Total Memory (B)",
                                        "vram_total_memory_b",
                                        "memory_total_bytes",
                                    ]:
                                        val = gpu_info.get(key)
                                        if val is not None:
                                            if isinstance(val, dict):
                                                memory_total_bytes = self._safe_int(
                                                    val, 0
                                                )
                                            else:
                                                memory_total_bytes = self._safe_int(
                                                    val, 0
                                                )
                                            break

                                    # Try different key names for used memory
                                    for key in [
                                        "VRAM Total Used Memory (B)",
                                        "vram_total_used_memory_b",
                                        "memory_used_bytes",
                                    ]:
                                        val = gpu_info.get(key)
                                        if val is not None:
                                            if isinstance(val, dict):
                                                memory_used_bytes = self._safe_int(
                                                    val, 0
                                                )
                                            else:
                                                memory_used_bytes = self._safe_int(
                                                    val, 0
                                                )
                                            break

                                    memory_total_mb = memory_total_bytes // (
                                        1024 * 1024
                                    )
                                    memory_used_mb = memory_used_bytes // (1024 * 1024)

                                    # Extract temperature - try multiple possible keys
                                    temp = 0
                                    for key in [
                                        "Temperature (Sensor edge) (C)",
                                        "temperature_c",
                                        "temp",
                                    ]:
                                        val = gpu_info.get(key)
                                        if val is not None:
                                            temp = self._safe_int(val, 0)
                                            break
                                    temp = min(max(temp, 0), 200)

                                    # Calculate derived values
                                    memory_used_gb = (
                                        round(memory_used_mb / 1024, 2)
                                        if memory_used_mb > 0
                                        else 0
                                    )
                                    memory_total_gb = (
                                        round(memory_total_mb / 1024, 2)
                                        if memory_total_mb > 0
                                        else 0
                                    )

                                    memory_usage_percent = 0.0
                                    if memory_total_mb > 0:
                                        memory_usage_percent = min(
                                            (memory_used_mb / memory_total_mb) * 100,
                                            100.0,
                                        )

                                    gpu_data.append(
                                        {
                                            "gpu_id": str(gpu_id),
                                            "name": name,
                                            "type": "AMD",
                                            "utilization_percent": utilization,
                                            "memory_used_mb": memory_used_mb,
                                            "memory_total_mb": memory_total_mb,
                                            "temperature_c": temp,
                                            "memory_used_gb": memory_used_gb,
                                            "memory_total_gb": memory_total_gb,
                                            "memory_usage_percent": round(
                                                memory_usage_percent, 2
                                            ),
                                        }
                                    )
                                except Exception as e:
                                    print(
                                        f"Warning: Error parsing AMD GPU {gpu_id}: {e}"
                                    )
                                    continue

                        if gpu_data:
                            return gpu_data

                    except json.JSONDecodeError:
                        continue  # Try next tool or fallback

            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue  # Try next tool
            except Exception as e:
                print(f"Debug: {tool_name} detection failed: {e}")
                continue  # Try next tool

        # Fallback to text parsing if JSON failed
        return self._get_amd_gpu_stats_fallback()

    def _get_amd_gpu_stats_fallback(self) -> Optional[List[Dict[str, Any]]]:
        """Fallback method for AMD GPU detection using text parsing"""
        try:
            with self.safe_subprocess(
                ["rocm-smi"],
                timeout=self.timeout_seconds,
            ) as process:
                stdout, stderr = process.communicate(timeout=self.timeout_seconds)
                if process.returncode != 0 or not stdout.strip():
                    return None
                gpu_data = []
                lines = stdout.strip().split("\n")

                # Look for GPU lines in rocm-smi output
                for line in lines:
                    if "GPU" in line and any(x in line for x in ["card", "device"]):
                        # Basic detection - extract what we can
                        gpu_match = re.search(r"GPU\[?(\d+)\]?", line, re.IGNORECASE)
                        gpu_id = gpu_match.group(1) if gpu_match else "0"

                        gpu_data.append(
                            {
                                "gpu_id": gpu_id,
                                "name": f"AMD GPU {gpu_id}",
                                "type": "AMD",
                                "utilization_percent": "N/A",
                                "memory_used_mb": "N/A",
                                "memory_total_mb": "N/A",
                                "temperature_c": "N/A",
                                "memory_used_gb": "N/A",
                                "memory_total_gb": "N/A",
                                "memory_usage_percent": "N/A",
                                "note": "AMD GPU detected - limited metrics available",
                            }
                        )

                return gpu_data if gpu_data else None
        except Exception as e:
            print(f"Debug: AMD fallback detection failed: {e}")
            return None

    def _get_intel_gpu_stats(self) -> Optional[List[Dict[str, Any]]]:
        """Get Intel GPU statistics with robust error handling"""
        gpu_data = []

        # Windows-specific detection methods
        if platform.system() == "Windows":
            # Method 1: Try WMI via wmic (Windows)
            try:
                with self.safe_subprocess(
                    [
                        "wmic",
                        "path",
                        "win32_VideoController",
                        "get",
                        "name,AdapterRAM",
                        "/format:list",
                    ],
                    timeout=self.timeout_seconds,
                ) as process:
                    stdout, stderr = process.communicate(timeout=self.timeout_seconds)
                    if process.returncode == 0 and stdout.strip():
                        lines = stdout.strip().split("\n")
                        current_gpu = {}
                        for line in lines:
                            line = line.strip()

                            # Check if this is a new GPU entry (empty line or new Name=)
                            if line == "":
                                # Process current GPU if it's Intel
                                if current_gpu.get("name") and (
                                    "Intel" in current_gpu["name"]
                                    or "Iris" in current_gpu["name"]
                                ):
                                    gpu_name = current_gpu["name"]
                                    memory_total_mb = current_gpu.get(
                                        "memory_total_mb", 0
                                    )
                                    memory_total_gb = (
                                        round(memory_total_mb / 1024, 2)
                                        if memory_total_mb > 0
                                        else "N/A"
                                    )

                                    gpu_data.append(
                                        {
                                            "gpu_id": "0",
                                            "name": gpu_name,
                                            "type": "Intel",
                                            "utilization_percent": "N/A",
                                            "memory_used_mb": "N/A",
                                            "memory_total_mb": memory_total_mb
                                            if memory_total_mb > 0
                                            else "N/A",
                                            "temperature_c": "N/A",
                                            "memory_used_gb": "N/A",
                                            "memory_total_gb": memory_total_gb,
                                            "memory_usage_percent": "N/A",
                                            "note": "Intel GPU detected via WMI (Windows)",
                                        }
                                    )
                                current_gpu = {}  # Reset for next GPU
                                continue

                            if line.startswith("Name="):
                                # If we already have a GPU, process it first
                                if current_gpu.get("name") and (
                                    "Intel" in current_gpu["name"]
                                    or "Iris" in current_gpu["name"]
                                ):
                                    gpu_name = current_gpu["name"]
                                    memory_total_mb = current_gpu.get(
                                        "memory_total_mb", 0
                                    )
                                    memory_total_gb = (
                                        round(memory_total_mb / 1024, 2)
                                        if memory_total_mb > 0
                                        else "N/A"
                                    )

                                    gpu_data.append(
                                        {
                                            "gpu_id": "0",
                                            "name": gpu_name,
                                            "type": "Intel",
                                            "utilization_percent": "N/A",
                                            "memory_used_mb": "N/A",
                                            "memory_total_mb": memory_total_mb
                                            if memory_total_mb > 0
                                            else "N/A",
                                            "temperature_c": "N/A",
                                            "memory_used_gb": "N/A",
                                            "memory_total_gb": memory_total_gb,
                                            "memory_usage_percent": "N/A",
                                            "note": "Intel GPU detected via WMI (Windows)",
                                        }
                                    )
                                current_gpu = {"name": line.split("=", 1)[1].strip()}
                            elif line.startswith("AdapterRAM="):
                                ram_bytes = line.split("=", 1)[1].strip()
                                if ram_bytes and ram_bytes != "":
                                    try:
                                        ram_mb = int(ram_bytes) // (1024 * 1024)
                                        current_gpu["memory_total_mb"] = ram_mb
                                    except (ValueError, TypeError):
                                        pass

                        # Process last GPU if it's Intel
                        if current_gpu.get("name") and (
                            "Intel" in current_gpu["name"]
                            or "Iris" in current_gpu["name"]
                        ):
                            gpu_name = current_gpu["name"]
                            memory_total_mb = current_gpu.get("memory_total_mb", 0)
                            memory_total_gb = (
                                round(memory_total_mb / 1024, 2)
                                if memory_total_mb > 0
                                else "N/A"
                            )

                            gpu_data.append(
                                {
                                    "gpu_id": "0",
                                    "name": gpu_name,
                                    "type": "Intel",
                                    "utilization_percent": "N/A",
                                    "memory_used_mb": "N/A",
                                    "memory_total_mb": memory_total_mb
                                    if memory_total_mb > 0
                                    else "N/A",
                                    "temperature_c": "N/A",
                                    "memory_used_gb": "N/A",
                                    "memory_total_gb": memory_total_gb,
                                    "memory_usage_percent": "N/A",
                                    "note": "Intel GPU detected via WMI (Windows)",
                                }
                            )

                        if gpu_data:
                            return gpu_data
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
            except Exception as e:
                print(f"Debug: Intel WMI detection failed: {e}")

            # Method 2: Try PowerShell (Windows)
            try:
                ps_command = (
                    "Get-WmiObject Win32_VideoController | "
                    "Where-Object { $_.Name -like '*Intel*' -or $_.Name -like '*Iris*' } | "
                    "Select-Object Name, AdapterRAM | "
                    "ConvertTo-Json"
                )
                with self.safe_subprocess(
                    ["powershell", "-Command", ps_command],
                    timeout=self.timeout_seconds,
                ) as process:
                    stdout, stderr = process.communicate(timeout=self.timeout_seconds)
                    if process.returncode == 0 and stdout.strip():
                        try:
                            data = json.loads(stdout)
                            # PowerShell might return array or single object
                            if isinstance(data, list):
                                gpus = data
                            else:
                                gpus = [data]

                            for gpu in gpus:
                                if not isinstance(gpu, dict):
                                    continue

                                gpu_name = gpu.get("Name", "Intel GPU")
                                if "Intel" in gpu_name or "Iris" in gpu_name:
                                    adapter_ram = gpu.get("AdapterRAM")
                                    memory_total_mb = 0
                                    if adapter_ram:
                                        try:
                                            memory_total_mb = int(adapter_ram) // (
                                                1024 * 1024
                                            )
                                        except (ValueError, TypeError):
                                            pass

                                    memory_total_gb = (
                                        round(memory_total_mb / 1024, 2)
                                        if memory_total_mb > 0
                                        else "N/A"
                                    )

                                    gpu_data.append(
                                        {
                                            "gpu_id": "0",
                                            "name": gpu_name,
                                            "type": "Intel",
                                            "utilization_percent": "N/A",
                                            "memory_used_mb": "N/A",
                                            "memory_total_mb": memory_total_mb
                                            if memory_total_mb > 0
                                            else "N/A",
                                            "temperature_c": "N/A",
                                            "memory_used_gb": "N/A",
                                            "memory_total_gb": memory_total_gb,
                                            "memory_usage_percent": "N/A",
                                            "note": "Intel GPU detected via PowerShell (Windows)",
                                        }
                                    )

                            if gpu_data:
                                return gpu_data
                        except json.JSONDecodeError:
                            pass
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
            except Exception as e:
                print(f"Debug: Intel PowerShell detection failed: {e}")

            # If Windows methods failed, return None (don't try Linux methods)
            print("Debug: Intel GPU not detected on Windows")
            return None

        # Linux/macOS-specific detection methods
        # Method 1: Try intel_gpu_top with JSON output (newer versions)
        try:
            with self.safe_subprocess(
                ["intel_gpu_top", "-J", "-s", "100"],  # JSON output, 100ms sample
                timeout=self.timeout_seconds,
            ) as process:
                stdout, stderr = process.communicate(timeout=self.timeout_seconds)
                if process.returncode == 0 and stdout.strip():
                    try:
                        data = json.loads(stdout)

                        # Extract GPU info from JSON
                        engines = data.get("engines", {})

                        # Calculate average utilization
                        total_busy = sum(
                            engine.get("busy", 0) for engine in engines.values()
                        )
                        num_engines = len(engines)
                        avg_utilization = (
                            int((total_busy / num_engines)) if num_engines > 0 else 0
                        )

                        gpu_data.append(
                            {
                                "gpu_id": "0",
                                "name": "Intel GPU",
                                "type": "Intel",
                                "utilization_percent": min(avg_utilization, 100),
                                "memory_used_mb": "N/A",
                                "memory_total_mb": "N/A",
                                "temperature_c": "N/A",
                                "memory_used_gb": "N/A",
                                "memory_total_gb": "N/A",
                                "memory_usage_percent": "N/A",
                            }
                        )
                        return gpu_data
                    except json.JSONDecodeError:
                        pass
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        # Method 2: Try sysfs (Linux)
        try:
            import os
            import glob

            drm_cards = glob.glob("/sys/class/drm/card*/device/vendor")
            for vendor_path in drm_cards:
                try:
                    with open(vendor_path, "r") as f:
                        vendor_id = f.read().strip()

                    # Intel vendor ID is 0x8086
                    if vendor_id == "0x8086":
                        card_path = os.path.dirname(vendor_path)

                        # Try to get device name
                        device_name = "Intel GPU"
                        try:
                            with open(os.path.join(card_path, "device"), "r") as f:
                                device_id = f.read().strip()
                                device_name = f"Intel GPU ({device_id})"
                        except Exception:
                            pass

                        gpu_data.append(
                            {
                                "gpu_id": "0",
                                "name": device_name,
                                "type": "Intel",
                                "utilization_percent": "N/A",
                                "memory_used_mb": "N/A",
                                "memory_total_mb": "N/A",
                                "temperature_c": "N/A",
                                "memory_used_gb": "N/A",
                                "memory_total_gb": "N/A",
                                "memory_usage_percent": "N/A",
                                "note": "Intel GPU detected via sysfs",
                            }
                        )
                        return gpu_data
                except Exception:
                    continue

        except Exception as e:
            print(f"Debug: Intel sysfs detection failed: {e}")

        # Method 3: Try lspci as last resort
        try:
            with self.safe_subprocess(
                ["lspci", "-nn"],
                timeout=self.timeout_seconds,
            ) as process:
                stdout, stderr = process.communicate(timeout=self.timeout_seconds)
                if process.returncode == 0 and stdout.strip():
                    for line in stdout.strip().split("\n"):
                        if "VGA" in line or "3D" in line or "Display" in line:
                            if "Intel" in line:
                                gpu_data.append(
                                    {
                                        "gpu_id": "0",
                                        "name": "Intel GPU (detected via lspci)",
                                        "type": "Intel",
                                        "utilization_percent": "N/A",
                                        "memory_used_mb": "N/A",
                                        "memory_total_mb": "N/A",
                                        "temperature_c": "N/A",
                                        "memory_used_gb": "N/A",
                                        "memory_total_gb": "N/A",
                                        "memory_usage_percent": "N/A",
                                        "note": "Intel GPU detected - install intel_gpu_top for detailed metrics",
                                    }
                                )
                                return gpu_data
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        print("Debug: Intel GPU not detected")
        return None

    def get_cuda_processes(self) -> Dict[str, Any]:
        """Get CUDA process information with robust error handling"""
        try:
            with self.safe_subprocess(
                [
                    "nvidia-smi",
                    "--query-compute-apps=gpu_name,pid,process_name,used_memory",
                    "--format=csv,noheader,nounits",
                ],
                timeout=self.timeout_seconds,
            ) as process:
                stdout, stderr = process.communicate(timeout=self.timeout_seconds)

                if process.returncode != 0:
                    print(f"Debug: nvidia-smi CUDA processes failed: {stderr}")
                    return {"message": "CUDA process information not available"}

                if not stdout.strip():
                    return {"message": "No active CUDA processes"}

            cuda_processes = []
            lines = stdout.strip().split("\n")

            for line_num, line in enumerate(lines):
                if not line.strip():
                    continue

                try:
                    parts = [part.strip() for part in line.split(",")]
                    if len(parts) < 4:
                        print(
                            f"Warning: Invalid CUDA process line {line_num + 1}: {line}"
                        )
                        continue

                    # Parse and validate each field
                    gpu_name = str(parts[0]) if parts[0] else "Unknown GPU"
                    pid = str(parts[1]) if parts[1] else "0"
                    process_name = str(parts[2]) if parts[2] else "Unknown Process"

                    # Parse memory usage
                    memory_used_mb = self._safe_int(parts[3], 0)
                    memory_used_mb = self._validate_positive_number(
                        memory_used_mb, f"CUDA process {pid} memory"
                    )

                    # Calculate GB
                    memory_used_gb = (
                        round(memory_used_mb / 1024, 2) if memory_used_mb > 0 else 0
                    )

                    cuda_processes.append(
                        {
                            "gpu_name": gpu_name,
                            "pid": pid,
                            "process_name": process_name,
                            "memory_used_mb": memory_used_mb,
                            "memory_used_gb": memory_used_gb,
                        }
                    )

                except Exception as e:
                    print(
                        f"Warning: Error parsing CUDA process line {line_num + 1}: {e}"
                    )
                    continue

            return (
                cuda_processes
                if cuda_processes
                else {"message": "No valid CUDA process data found"}
            )

        except subprocess.TimeoutExpired:
            print("Warning: nvidia-smi CUDA processes command timed out")
            return {"message": "CUDA process information not available"}
        except FileNotFoundError:
            print("Debug: nvidia-smi command not found")
            return {"message": "CUDA process information not available"}
        except Exception as e:
            print(f"Error: CUDA process error: {e}")
            return {"error": f"CUDA process error: {str(e)}"}

    def get_system_info(self):
        """Get basic system information"""
        try:
            import psutil

            return {
                "hostname": platform.node(),
                "os": f"{platform.system()} {platform.release()}",
                "architecture": platform.machine(),
                "python_version": platform.python_version(),
                "monitor_version": __version__,
                "uptime_seconds": round(time.time() - psutil.boot_time(), 2),
                "boot_time": time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(psutil.boot_time())
                ),
            }
        except ImportError:
            return {
                "hostname": platform.node(),
                "os": f"{platform.system()} {platform.release()}",
                "architecture": platform.machine(),
                "python_version": platform.python_version(),
                "monitor_version": __version__,
                "uptime_seconds": "Unknown (psutil not available)",
                "boot_time": "Unknown (psutil not available)",
            }
        except Exception as e:
            return {"error": f"System info not available: {str(e)}"}

    def get_all_metrics(self):
        """Get all server metrics"""
        metrics = {
            "timestamp": time.time(),
            "formatted_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "system_info": self.get_system_info(),
            "cpu": self.get_cpu_usage(),
            "memory": self.get_memory_usage(),
            "disk": self.get_disk_usage(),
            "network": self.get_network_usage(),
            "gpu": self.get_gpu_stats(),
            "cuda_processes": self.get_cuda_processes(),
        }

        return metrics


def emit_metrics_to_server():
    """Emit metrics to Socket.IO server at regular intervals with built-in reconnection"""
    try:
        from threading import Event

        # Create stop event for graceful shutdown
        stop_event = Event()

        # Create Socket.IO client with built-in reconnection
        sio = socketio.Client(
            reconnection=True,
            reconnection_attempts=10,  # 10 attempts after first successful connection
            reconnection_delay=1,
            reconnection_delay_max=30,  # Max 30 seconds between retries
            logger=True,  # Enable logging for debugging
        )

        # Connection event handler
        @sio.event
        def connect():
            print(f"[OK] Connected to Socket.IO server: {SOCKET_SERVER_URL}")
            print(f"[INFO] Server ID: {SERVER_ID}")
            print(f"[INFO] Emitting metrics every {TIME_INTERVAL} seconds...")
            print("Press Ctrl+C to stop...")

        # Disconnection event handler
        @sio.event
        def disconnect():
            print("[ERROR] Disconnected from Socket.IO server")

        # Error event handler
        @sio.event
        def connect_error(data):
            print(f"[ERROR] Connection error: {data}")

        # Connect to server with retry logic
        def connect_with_retry(url, max_retries=5):
            """Connect to server with retry logic"""
            retries = 0
            while max_retries is None or retries < max_retries:
                try:
                    sio.connect(url)
                    return True
                except Exception as e:
                    retries += 1
                    print(f"[RETRY] Connection attempt {retries} failed: {e}")
                    if retries < max_retries:
                        time.sleep(2)
                    else:
                        print(f"[ERROR] Failed to connect after {max_retries} attempts")
                        return False
            return False

        # Initial connection
        full_url = f"{SOCKET_SERVER_URL}?serverId={SERVER_ID}"
        if not connect_with_retry(full_url, max_retries=5):
            print("[ERROR] Could not establish initial connection")
            return False

        # Create metrics collector
        metrics_collector = ServerMetrics()

        # Main metrics emission loop
        def send_metrics():
            """Send metrics at regular intervals"""
            consecutive_failures = 0
            max_consecutive_failures = 10  # Exit after 10 consecutive failures

            while not stop_event.is_set():
                try:
                    if sio.connected:
                        # Collect metrics
                        metrics = metrics_collector.get_all_metrics()

                        # Add server ID to metrics
                        metrics["server_id"] = SERVER_ID

                        # Emit to server
                        sio.emit("server-stats", metrics)
                        print(f"[INFO] Metrics emitted at {metrics['formatted_time']}")
                        consecutive_failures = 0  # Reset failure counter on success
                    else:
                        print("[WARNING] Not connected, waiting for reconnection...")
                        consecutive_failures += 1

                        # Check if we've had too many consecutive failures
                        if consecutive_failures >= max_consecutive_failures:
                            print(
                                f"[ERROR] Too many consecutive connection failures ({consecutive_failures}), exiting..."
                            )
                            break

                    # Wait for next interval or stop event
                    for _ in range(
                        TIME_INTERVAL * 10
                    ):  # Check stop_event every 0.1 seconds
                        if stop_event.is_set():
                            break
                        time.sleep(0.1)

                except Exception as e:
                    print(f"[ERROR] Error in metrics loop: {e}")
                    consecutive_failures += 1
                    time.sleep(1)

        try:
            # Start sending metrics
            send_metrics()
        except KeyboardInterrupt:
            print("\n[STOP] Stopping metrics emission...")
            stop_event.set()
        finally:
            # Clean disconnect
            if sio.connected:
                sio.disconnect()
            print("[OK] Cleaned up connection")

        return True

    except ImportError:
        print(
            "[ERROR] python-socketio module not found. Install with: pip install python-socketio"
        )
        return False
    except Exception as e:
        print(f"[ERROR] Error in main loop: {str(e)}")
        return False


def get_user_config():
    """Ask user for configuration"""
    print("System Metrics Easy - Simple Setup")
    print("=" * 50)

    # Get time interval
    print("1. How often to collect metrics?")
    print("   Default: 10 seconds")
    interval = input("   Enter interval in seconds (or press Enter for 10): ").strip()
    if not interval:
        interval = "10"

    # Server URL is hardcoded
    server_url = "https://api.server-metrics.letz.chat"
    # server_url = "http://localhost:8000"

    print(f"\n2. Backend server: {server_url} (hardcoded)")

    # Get server ID
    hostname = platform.node()
    print("\n3. What should we call this server?")
    print(f"   Default: server-{hostname}")
    server_id = input("   Enter server name (or press Enter for default): ").strip()
    if not server_id:
        server_id = f"server-{hostname}"

    return interval, server_url, server_id


def run_in_background(interval, server_url, server_id):
    """Run the server metrics monitor in background"""
    print("\nStarting System Metrics Easy in background...")
    print(f"   Interval: {interval} seconds")
    print(f"   Server: {server_url}")
    print(f"   Server ID: {server_id}")

    # Get the path to the main script
    script_dir = Path(__file__).parent.parent
    main_script = script_dir / "system_metrics_easy" / "server_metrics.py"

    if not main_script.exists():
        print("[ERROR] Main script not found!")
        return False

    # Create log file
    log_file = script_dir / "system-metrics-easy.log"

    try:
        # Set environment variables
        env = os.environ.copy()
        env["TIME_INTERVAL"] = interval
        env["SOCKET_SERVER_URL"] = server_url
        env["SERVER_ID"] = server_id

        # Run the script in background with output to log file
        with open(log_file, "w") as f:
            process = subprocess.Popen(
                [sys.executable, str(main_script), "--foreground"],
                stdout=f,
                stderr=subprocess.STDOUT,
                cwd=str(script_dir),
                env=env,
                start_new_session=True,  # This detaches the process from the parent
            )

        # Give it a moment to start
        time.sleep(1)

        # Check if process is still running
        if process.poll() is None:
            # Save PID to file
            pid_file = script_dir / "system-metrics-easy.pid"
            with open(pid_file, "w") as f:
                f.write(str(process.pid))

            print("[OK] System Metrics Easy started!")
            print(f"[INFO] PID: {process.pid}")
            print(f"[INFO] Logs: {log_file}")
            print("[INFO] To stop: system-metrics-easy --stop")
            print("[INFO] To check: system-metrics-easy --status")

            return True
        else:
            print(f"[ERROR] Process failed to start. Check logs: {log_file}")
            return False

    except Exception as e:
        print(f"[ERROR] Error starting: {e}")
        return False


def stop_background():
    """Stop the background process"""
    script_dir = Path(__file__).parent.parent
    pid_file = script_dir / "system-metrics-easy.pid"

    if not pid_file.exists():
        print("[WARNING] No PID file found. Process may not be running.")
        return False

    try:
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())

        # Try to terminate the process
        os.kill(pid, signal.SIGTERM)
        time.sleep(1)

        # Check if still running
        try:
            os.kill(pid, 0)  # This will raise an exception if process doesn't exist
            print("[WARNING] Process still running, force killing...")
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass  # Process already stopped

        # Remove PID file
        pid_file.unlink()

        print("[OK] System Metrics Easy stopped!")
        return True

    except Exception as e:
        print(f"[ERROR] Error stopping: {e}")
        return False


def check_status():
    """Check if the process is running"""
    script_dir = Path(__file__).parent.parent
    pid_file = script_dir / "system-metrics-easy.pid"
    log_file = script_dir / "system-metrics-easy.log"

    if not pid_file.exists():
        print("[ERROR] System Metrics Easy is not running")
        return False

    try:
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())

        # Check if process is still running
        try:
            os.kill(pid, 0)  # This will raise an exception if process doesn't exist
            print(f"[OK] System Metrics Easy is running (PID: {pid})")

            if log_file.exists():
                print(f"[INFO] Log file: {log_file}")
                print("[INFO] Recent logs:")
                print("-" * 40)
                try:
                    with open(log_file, "r") as f:
                        lines = f.readlines()
                        for line in lines[-10:]:  # Last 10 lines
                            print(line.rstrip())
                except Exception:
                    print("Could not read log file")

            return True
        except OSError:
            print("[ERROR] Process is not running (stale PID file)")
            pid_file.unlink()  # Remove stale PID file
            return False

    except Exception as e:
        print(f"[ERROR] Error checking status: {e}")
        return False


def main():
    """Main function - Simple background process management"""
    global TIME_INTERVAL, SOCKET_SERVER_URL, SERVER_ID

    parser = argparse.ArgumentParser(
        description="System Metrics Easy - Simple Background Process",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--foreground", action="store_true", help="Run in foreground (internal use)"
    )
    parser.add_argument(
        "--status", action="store_true", help="Check if process is running"
    )
    parser.add_argument(
        "--stop", action="store_true", help="Stop the background process"
    )

    args = parser.parse_args()

    if args.stop:
        # Stop background process
        return stop_background()
    elif args.status:
        # Check status
        return check_status()
    elif args.foreground:
        # Run in foreground (called by background process)
        # Update global variables from environment
        TIME_INTERVAL = int(os.getenv("TIME_INTERVAL", "10"))
        # SOCKET_SERVER_URL is hardcoded, no need to read from environment
        SERVER_ID = os.getenv("SERVER_ID", f"server-{platform.node()}")

        print("Starting System Metrics Easy")
        print(f"   Interval: {TIME_INTERVAL} seconds")
        print(f"   Server: {SOCKET_SERVER_URL}")
        print(f"   Server ID: {SERVER_ID}")

        # Emit to Socket.IO server
        return emit_metrics_to_server()
    else:
        # Interactive configuration and start
        print("System Metrics Easy - Simple Setup")
        print("=" * 50)

        # Get configuration
        interval, server_url, server_id = get_user_config()

        print("\n[OK] Configuration:")
        print(f"   Interval: {interval} seconds")
        print(f"   Server: {server_url}")
        print(f"   Server ID: {server_id}")

        # Ask if user wants to start now
        start_now = input("\nStart monitoring now? (y/n): ").strip().lower()
        if start_now in ["y", "yes", ""]:
            # Run in background
            return run_in_background(interval, server_url, server_id)
        else:
            print("[INFO] To start later, run: system-metrics-easy")
            return True


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Device utility functions for PyTorch

Provides functions for detecting available compute devices (CPU, CUDA, MPS, XPU)
"""

# Cache device types to avoid repeated torch imports (expensive ~9-11s)
_cached_device_types = None


def _available_device_types() -> list[str]:
    """
    Get list of available PyTorch device types (cached after first call)

    Returns:
        List of available device types, ordered by preference (CUDA first if available, CPU last)
    """
    global _cached_device_types

    # Return cached result if available
    if _cached_device_types is not None:
        return _cached_device_types

    devices = ["cpu"]

    try:
        import torch

        if torch.cuda.is_available():
            devices.insert(0, "cuda")

        if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
            cuda_pos = devices.index("cuda") if "cuda" in devices else 0
            devices.insert(cuda_pos + 1, "mps")

        if getattr(torch, "xpu", None) and torch.xpu.is_available():
            cpu_pos = devices.index("cpu")
            devices.insert(cpu_pos, "xpu")
    except Exception:
        # PyTorch not installed or error checking devices - just return CPU
        pass

    # Cache the result
    _cached_device_types = devices
    return devices

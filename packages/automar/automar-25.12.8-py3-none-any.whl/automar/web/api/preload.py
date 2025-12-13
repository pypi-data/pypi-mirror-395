"""
Module preloading utilities to improve API startup performance.

Heavy ML libraries (sklearn, ray, torch) are preloaded in background subprocesses
to avoid blocking the main API startup while still benefiting from OS page cache.
"""

import threading
import time

# Module preloading state
_lightweight_modules_preloaded = False
_torch_preloaded = False
_preload_lock = threading.Lock()


def preload_lightweight_modules():
    """Preload sklearn and ray in subprocess (non-blocking)"""
    global _lightweight_modules_preloaded

    with _preload_lock:
        if _lightweight_modules_preloaded:
            return

        print(
            "[INFO] Preloading lightweight ML modules (sklearn, ray) in background..."
        )

        # Use subprocess for zero GIL contention
        import subprocess
        import sys

        subprocess.Popen(
            [
                sys.executable,
                "-c",
                "import sklearn.preprocessing; import ray; print('[INFO] Lightweight modules cached')",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        _lightweight_modules_preloaded = True
        print(f"[INFO] Lightweight module preload started (background, ~5s)")


def preload_torch():
    """Preload torch in subprocess (non-blocking)"""
    global _torch_preloaded

    with _preload_lock:
        if _torch_preloaded:
            return

        print("[INFO] Preloading torch in background...")

        # Use subprocess for zero GIL contention
        import subprocess
        import sys

        subprocess.Popen(
            [sys.executable, "-c", "import torch; print('[INFO] Torch cached')"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        _torch_preloaded = True
        print(f"[INFO] Torch preload started (background, ~9-11s)")

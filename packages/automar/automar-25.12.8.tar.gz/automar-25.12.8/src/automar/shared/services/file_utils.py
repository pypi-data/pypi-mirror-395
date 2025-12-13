# -*- coding: utf-8 -*-
"""File system utility functions for opening folders and managing files."""
import os
import platform
import subprocess
import sys
import importlib.util
from pathlib import Path


def open_folder_in_explorer(folder_path: Path) -> bool:
    """
    Open a folder in the system's file explorer asynchronously.

    This function launches the file explorer in a non-blocking way to avoid
    clogging the API server thread. The file explorer opens in a separate process
    that runs independently of the API.

    Args:
        folder_path: Path object pointing to the folder to open

    Returns:
        True if successful, False otherwise

    Raises:
        FileNotFoundError: If the folder doesn't exist
        RuntimeError: If the operation fails or OS is unsupported
    """
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder_path}")

    if not folder_path.is_dir():
        raise ValueError(f"Path is not a directory: {folder_path}")

    system = platform.system()

    try:
        if system == "Windows":
            # Use subprocess.Popen instead of os.startfile for async behavior
            # explorer.exe is non-blocking and runs independently
            subprocess.Popen(["explorer", str(folder_path)])
        elif system == "Darwin":  # macOS
            # Run in background without waiting for completion
            subprocess.Popen(["open", str(folder_path)])
        elif system == "Linux":
            # Run in background without waiting for completion
            subprocess.Popen(["xdg-open", str(folder_path)])
        else:
            raise RuntimeError(f"Unsupported operating system: {system}")

        return True

    except Exception as e:
        raise RuntimeError(f"Error opening folder: {e}")


def load_module_with_functions(file_path, required_functions=None):
    """
    Dynamically load a Python file and verify it contains specific functions.

    Args:
        file_path (str): Path to the Python file to load
        required_functions (list): List of function names that must exist in the module

    Returns:
        module: The loaded module if successful, None otherwise
    """
    if not os.path.isfile(file_path):
        print(f"Error: File {file_path} does not exist")
        return None

    if not str(file_path).endswith(".py"):
        print(f"Error: {file_path} is not a Python file")
        return None

    required_functions = required_functions or []

    try:
        module_name = os.path.basename(file_path).replace(".py", "")

        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            print(f"Error: Could not load spec from {file_path}")
            return None

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

    except ImportError as e:
        print(f"Import error: {str(e)}")
        return None
    except SyntaxError as e:
        print(f"Syntax error in the module: {str(e)}")
        return None
    except ModuleNotFoundError as e:
        print(f"Missing dependency: {str(e)}")
        return None

    missing_functions = []
    for func_name in required_functions:
        try:
            if not hasattr(module, func_name) or not callable(
                getattr(module, func_name)
            ):
                missing_functions.append(func_name)
        except AttributeError as e:
            print(f"Error checking function {func_name}: {str(e)}")
            return None

    if missing_functions:
        print(
            f"Error: Module is missing required functions: {', '.join(missing_functions)}"
        )
        return None

    return module

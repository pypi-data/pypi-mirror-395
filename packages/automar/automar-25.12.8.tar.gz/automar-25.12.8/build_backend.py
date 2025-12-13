"""Custom build backend for Automar package.

This is a PEP 517 compliant build backend that extends setuptools.build_meta
to optionally build the SvelteKit frontend before creating wheels.

Usage:
    BUILD_WEB=0 python -m build    # API-only package (default, faster)
    BUILD_WEB=1 python -m build    # Full package with web UI (requires npm)

The BUILD_WEB environment variable controls whether the frontend is built.
When BUILD_WEB=1, Node.js and npm must be installed on the build system.

This backend acts as a transparent wrapper around setuptools.build_meta,
intercepting only the build_wheel hook to inject frontend compilation.
All other hooks are passed through unchanged.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Import the standard setuptools build backend
from setuptools import build_meta as _orig

# Re-export all standard PEP 517 hooks unchanged
# These handle sdist creation, metadata generation, etc.
get_requires_for_build_wheel = _orig.get_requires_for_build_wheel
get_requires_for_build_sdist = _orig.get_requires_for_build_sdist
prepare_metadata_for_build_wheel = _orig.prepare_metadata_for_build_wheel

# Export editable install hooks (PEP 660) - we'll wrap build_editable below
try:
    get_requires_for_build_editable = _orig.get_requires_for_build_editable
    prepare_metadata_for_build_editable = _orig.prepare_metadata_for_build_editable
    _orig_build_editable = _orig.build_editable
except AttributeError:
    # Older setuptools versions don't have editable hooks
    _orig_build_editable = None

_FRONTEND_BUILT = False
_SKIP_MESSAGE_SHOWN = False


def _should_build_web():
    """Check if BUILD_WEB environment variable is set to '1'."""
    return os.environ.get("BUILD_WEB", "0") == "1"


def _run_npm_command(args, cwd=None, capture_output=True, text=True):
    """Run npm command with cross-platform compatibility."""
    is_windows = sys.platform == "win32"
    return subprocess.run(
        args,
        cwd=cwd,
        capture_output=capture_output,
        text=text,
        check=True,
        shell=is_windows,
    )


def _build_frontend():
    """Build SvelteKit frontend directly to src/automar/web/static/.

    This function:
    1. Checks if npm is installed
    2. Installs frontend dependencies with 'npm ci'
    3. Builds the production frontend with 'npm run build'
    4. Outputs directly to src/automar/web/static/ (configured in svelte.config.js)

    Raises:
        RuntimeError: If npm is not found or build fails
    """
    print("\n" + "=" * 70)
    print("  Building Web Frontend (BUILD_WEB=1)")
    print("=" * 70)

    frontend_dir = Path("frontend")
    build_dir = Path("src") / "automar" / "web" / "static"

    # Verify npm is available
    try:
        result = _run_npm_command(["npm", "--version"])
        npm_version = result.stdout.strip()
        print(f"\n[OK] Found npm version: {npm_version}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise RuntimeError(
            "\n"
            "ERROR: npm is not installed or not in PATH\n"
            "\n"
            "The web UI build requires Node.js and npm.\n"
            "\n"
            "Options:\n"
            "  1. Install Node.js from https://nodejs.org/\n"
            "  2. Build without web UI: BUILD_WEB=0 python -m build\n"
            "\n"
            f"Error details: {e}\n"
        )

    # Verify frontend directory exists
    if not frontend_dir.exists():
        raise RuntimeError(
            f"\n"
            f"ERROR: Frontend source directory not found: {frontend_dir}\n"
            f"\n"
            f"Cannot build web UI without frontend source code.\n"
            f"Are you building from a complete source checkout?\n"
        )

    # Clean previous build
    if build_dir.exists():
        print(f"[OK] Cleaning previous build: {build_dir}")
        shutil.rmtree(build_dir)

    # Install npm dependencies
    print(f"\n[*] Installing frontend dependencies...")
    print(f"    Running: npm ci")
    try:
        _run_npm_command(["npm", "ci"], cwd=frontend_dir)
        print("[OK] Dependencies installed")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"\n"
            f"ERROR: npm ci failed\n"
            f"\n"
            f"STDOUT:\n{e.stdout}\n"
            f"\n"
            f"STDERR:\n{e.stderr}\n"
        )

    # Build frontend
    print(f"\n[*] Building production frontend...")
    print(f"    Running: npm run build")
    try:
        _run_npm_command(["npm", "run", "build"], cwd=frontend_dir)
        print("[OK] Frontend built successfully")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"\n"
            f"ERROR: npm run build failed\n"
            f"\n"
            f"STDOUT:\n{e.stdout}\n"
            f"\n"
            f"STDERR:\n{e.stderr}\n"
        )

    # Verify build output
    if not build_dir.exists():
        raise RuntimeError(
            f"\n"
            f"ERROR: Build directory not created: {build_dir}\n"
            f"\n"
            f"The frontend build completed but did not create the expected\n"
            f"output directory. Check the frontend build configuration.\n"
        )

    # Verify critical files
    index_html = build_dir / "index.html"
    if not index_html.exists():
        raise RuntimeError(
            f"\n"
            f"ERROR: index.html not found in build output\n"
            f"\n"
            f"Expected: {index_html}\n"
            f"\n"
            f"The frontend build may be incomplete or misconfigured.\n"
        )

    # Count files for user feedback
    file_count = len(list(build_dir.rglob("*")))
    total_size = sum(f.stat().st_size for f in build_dir.rglob("*") if f.is_file())
    size_mb = total_size / (1024 * 1024)

    print(f"[OK] Built {file_count} files ({size_mb:.1f} MB) in {build_dir}")
    print(f"    Frontend ready for packaging in: {build_dir}")

    print("\n" + "=" * 70)
    print("  [OK] Web Frontend Build Complete")
    print("=" * 70 + "\n")


def _build_frontend_if_requested():
    """Build frontend if BUILD_WEB=1, otherwise print skip message."""
    global _FRONTEND_BUILT, _SKIP_MESSAGE_SHOWN
    if not _should_build_web():
        if not _SKIP_MESSAGE_SHOWN:
            print("\n[*] Skipping web frontend build (BUILD_WEB=0)")
            print("    Package will be created without web UI\n")
            _SKIP_MESSAGE_SHOWN = True
        return False
    if _FRONTEND_BUILT:
        return False

    frontend_dir = Path("frontend")
    build_dir = Path("src") / "automar" / "web" / "static"
    if not frontend_dir.exists():
        if build_dir.exists():
            print(
                "\n[!] Frontend sources not found; using existing compiled assets in "
                f"{build_dir}\n",
            )
            _FRONTEND_BUILT = True
            return False
        raise RuntimeError(
            "\nERROR: Frontend source directory not found and no prebuilt assets are available.\n"
            "Cannot build web UI without frontend source code. Are you building from a complete source checkout?\n",
        )

    _build_frontend()
    _FRONTEND_BUILT = True
    return True


def _cleanup_build_artifacts():
    """Clean up temporary build artifacts after wheel creation.

    Removes the build/ directory that setuptools creates during the build process.
    This directory is temporary and should not persist after installation.
    """
    build_dir = Path("build")
    if build_dir.exists():
        print(f"\n[*] Cleaning up temporary build artifacts: {build_dir}")
        try:
            shutil.rmtree(build_dir)
            print(f"[OK] Build artifacts removed")
        except Exception as e:
            print(f"[WARNING] Could not remove build directory: {e}")


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    """PEP 517 build_wheel hook with optional frontend compilation.

    Args:
        wheel_directory: Directory where the wheel should be written
        config_settings: Optional config settings from build frontend
        metadata_directory: Optional metadata directory from prepare step

    Returns:
        Filename of the built wheel
    """
    _build_frontend_if_requested()
    result = _orig.build_wheel(wheel_directory, config_settings, metadata_directory)
    _cleanup_build_artifacts()
    return result


def build_sdist(sdist_directory, config_settings=None):
    """Ensure frontend assets exist before creating the source distribution."""
    _build_frontend_if_requested()
    return _orig.build_sdist(sdist_directory, config_settings)


def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
    """PEP 660 build_editable hook for 'pip install -e .' with optional frontend.

    Args:
        wheel_directory: Directory where the wheel should be written
        config_settings: Optional config settings from build frontend
        metadata_directory: Optional metadata directory from prepare step

    Returns:
        Filename of the built editable wheel
    """
    if _orig_build_editable is None:
        raise RuntimeError("Editable installs not supported by this setuptools version")

    _build_frontend_if_requested()
    result = _orig_build_editable(wheel_directory, config_settings, metadata_directory)
    _cleanup_build_artifacts()
    return result

"""GUI runner - starts API server and opens web browser."""

import webbrowser
import time
import threading
from pathlib import Path


def has_web_ui():
    """Check if web UI static files are available.

    Returns:
        bool: True if the web UI is installed, False otherwise.
    """
    from automar.shared.config.path_resolver import get_package_root

    # Frontend is always in automar/web/static/ (built by SvelteKit via svelte.config.js)
    package_static = get_package_root() / "web" / "static"
    return (package_static / "index.html").exists()


def run_gui(cfg):
    """Start API server and open web browser (requires web UI).

    Args:
        cfg: Configuration object with api settings (host, port, etc.)

    Returns:
        None
    """
    if not has_web_ui():
        print("\n" + "=" * 60)
        print("ERROR: Web UI is not available in this installation")
        print("=" * 60)
        print("\nThe 'automar gui' command requires the web UI static files,")
        print("which are not present in this installation.\n")
        print("This usually means the package was built without BUILD_WEB=1.\n")
        print("Options:")
        print("  1. Use API-only mode:  automar api")
        print("  2. Rebuild with web:   BUILD_WEB=1 pip install -e .")
        print("  3. Install from PyPI:  pip install automar")
        print("=" * 60 + "\n")
        return

    host = cfg.api.host
    port = cfg.api.port
    url = f"http://{host}:{port}"

    print("\n" + "=" * 60)
    print("Starting Automar Web UI")
    print("=" * 60)
    print(f"\n  API Server: {url}")
    print(f"  Web UI:     {url}")
    print(f"\n  Browser will open when server is ready...")
    print(f"  Press Ctrl+C to stop\n")
    print("=" * 60 + "\n")

    # Open browser after confirming server is ready
    def open_browser():
        import urllib.request
        import urllib.error

        # Wait up to 30 seconds for server to be ready
        max_wait = 30
        start_time = time.time()

        while time.time() - start_time < max_wait:
            try:
                # Try to connect to health endpoint
                urllib.request.urlopen(f"{url}/health", timeout=1)
                # Server is ready!
                break
            except (urllib.error.URLError, Exception):
                # Server not ready yet, wait a bit
                time.sleep(0.5)
        else:
            # Timeout - open browser anyway
            print(f"⚠ Server health check timed out after {max_wait}s")

        try:
            webbrowser.open(url)
            print(f"✓ Browser opened: {url}\n")
        except Exception as e:
            print(f"⚠ Could not open browser automatically: {e}")
            print(f"  Please open manually: {url}\n")

    threading.Thread(target=open_browser, daemon=True).start()

    # Import and start API server (blocks)
    from automar.shared.runners.api_runner import run_api

    run_api(cfg)

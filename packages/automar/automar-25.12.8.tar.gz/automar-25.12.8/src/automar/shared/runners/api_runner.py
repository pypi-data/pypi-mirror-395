# -*- coding: utf-8 -*-
"""
API server runner for Automar

Handles starting the FastAPI server with uvicorn
"""


def run_api(cfg):
    """
    Run the FastAPI server

    Args:
        cfg: Configuration object with API parameters

    Returns:
        None (runs the server until interrupted)
    """
    try:
        import uvicorn
    except ImportError:
        print("Error: uvicorn is not installed.")
        print("Please install it with: pip install 'uvicorn[standard]'")
        return

    from automar.web import app

    app_str = "automar.web.app:app"

    print(f"Starting API server on http://{cfg.api.host}:{cfg.api.port}")
    print(f"Documentation available at: http://{cfg.api.host}:{cfg.api.port}/docs")
    print("Press CTRL+C to stop")

    if cfg.api.workers > 1 and not cfg.api.reload:
        # Production mode with multiple workers
        uvicorn.run(
            app_str,
            host=cfg.api.host,
            port=cfg.api.port,
            workers=cfg.api.workers,
            log_level="info",
        )
    else:
        # Development mode
        uvicorn.run(
            app_str,
            host=cfg.api.host,
            port=cfg.api.port,
            reload=cfg.api.reload,
            log_level="info",
        )

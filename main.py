from fastapi import FastAPI
import uvicorn
import logging
import sys
from app.router.item import router as item_router
from app.container import Container

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI()

    # Initialize and wire the DI container
    container = Container()
    container.wire(modules=["app.router.item"])

    app.include_router(item_router, prefix="/api", tags=["item"])

    return app


# Create app at module level for import string reference in uvicorn
app = create_app()


def main():
    """Main entry point for running the FastAPI server."""
    # Get application config from DI container
    container = Container()
    app_config = container.app_config()

    # Get server configuration
    server_config = app_config.get_server_config()

    # When reload is enabled, uvicorn requires an import string instead of app object
    if server_config.get("reload", False):
        server_config_for_uvicorn = {
            k: v for k, v in server_config.items() if v is not None
        }
        uvicorn.run("main:app", **server_config_for_uvicorn)
    else:
        uvicorn.run(app, **server_config)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(130)

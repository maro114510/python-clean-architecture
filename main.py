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


def main():
    """Main entry point for running the FastAPI server."""
    app = create_app()
    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(130)

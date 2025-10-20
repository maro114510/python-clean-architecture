from fastapi import FastAPI
import uvicorn
import logging
import sys
from app.router.item import router as item_router

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(item_router, prefix="/api", tags=["item"])


def main():
    """Main entry point for running the FastAPI server."""
    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(130)

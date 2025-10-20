import os
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class AppConfig:
    """
    Application configuration class to hold application settings.
    """

    # Environment constants
    ENV_DEVELOPMENT = "development"
    ENV_PRODUCTION = "production"

    # Default values
    DEFAULT_ENV = ENV_DEVELOPMENT
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 8000
    DEFAULT_LOG_LEVEL_DEV = "debug"
    DEFAULT_LOG_LEVEL_PROD = "info"

    env: str
    host: str
    port: int
    log_level: str

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Load application configuration from environment variables."""
        env = os.getenv("ENV", cls.DEFAULT_ENV).lower()
        host = os.getenv("HOST", cls.DEFAULT_HOST)
        port = int(os.getenv("PORT", str(cls.DEFAULT_PORT)))

        # Set log level based on environment
        if env == cls.ENV_DEVELOPMENT:
            log_level = os.getenv("LOG_LEVEL", cls.DEFAULT_LOG_LEVEL_DEV)
        else:
            log_level = os.getenv("LOG_LEVEL", cls.DEFAULT_LOG_LEVEL_PROD)

        return cls(
            env=env,
            host=host,
            port=port,
            log_level=log_level,
        )

    @property
    def is_development(self) -> bool:
        """Check if the application is in development mode."""
        return self.env == self.ENV_DEVELOPMENT

    @property
    def is_production(self) -> bool:
        """Check if the application is in production mode."""
        return self.env == self.ENV_PRODUCTION

    def get_server_config(self) -> Dict[str, Any]:
        """Get uvicorn server configuration."""
        return {
            "host": self.host,
            "port": self.port,
            "reload": self.is_development,
            "reload_dirs": ["app"] if self.is_development else None,
            "log_level": self.log_level,
        }

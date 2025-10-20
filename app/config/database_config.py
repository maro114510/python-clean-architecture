import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """
    Database configuration class to hold database connection settings.
    """

    # Database type constants
    SQLITE = "sqlite"
    MYSQL = "mysql"
    FIRESTORE = "firestore"

    # Default values
    DEFAULT_SQLITE_PATH = "db.sqlite3"
    DEFAULT_MYSQL_HOST = "localhost"
    DEFAULT_MYSQL_PORT = 3306
    DEFAULT_MYSQL_USER = "root"
    DEFAULT_MYSQL_PASSWORD = ""
    DEFAULT_MYSQL_DATABASE = "test"

    db_type: str
    sqlite_path: Optional[str] = None
    mysql_host: Optional[str] = None
    mysql_port: Optional[int] = None
    mysql_user: Optional[str] = None
    mysql_password: Optional[str] = None
    mysql_database: Optional[str] = None
    firestore_project_id: Optional[str] = None
    firestore_credentials_path: Optional[str] = None

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        """Load database configuration from environment variables."""
        db_type = os.getenv("DB_TYPE", cls.SQLITE).lower()

        config = cls(db_type=db_type)

        if db_type == cls.SQLITE:
            config.sqlite_path = os.getenv("SQLITE_DB_PATH", cls.DEFAULT_SQLITE_PATH)

        elif db_type == cls.MYSQL:
            config.mysql_host = os.getenv("MYSQL_HOST", cls.DEFAULT_MYSQL_HOST)
            config.mysql_port = int(os.getenv("MYSQL_PORT", str(cls.DEFAULT_MYSQL_PORT)))
            config.mysql_user = os.getenv("MYSQL_USER", cls.DEFAULT_MYSQL_USER)
            config.mysql_password = os.getenv("MYSQL_PASSWORD", cls.DEFAULT_MYSQL_PASSWORD)
            config.mysql_database = os.getenv("MYSQL_DATABASE", cls.DEFAULT_MYSQL_DATABASE)

        elif db_type == cls.FIRESTORE:
            config.firestore_project_id = os.getenv("FIRESTORE_PROJECT_ID")
            config.firestore_credentials_path = os.getenv("FIRESTORE_CREDENTIALS_PATH")

        return config

    def get_connection_params(self) -> Dict[str, Any]:
        """Get connection parameters based on the database type."""
        if self.db_type == self.SQLITE:
            return {"db_path": self.sqlite_path}
        elif self.db_type == self.MYSQL:
            return {
                "host": self.mysql_host,
                "port": self.mysql_port,
                "user": self.mysql_user,
                "password": self.mysql_password,
                "database": self.mysql_database,
            }
        elif self.db_type == self.FIRESTORE:
            return {
                "project_id": self.firestore_project_id,
                "credentials_path": self.firestore_credentials_path,
            }
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")

from app.config.database_config import DatabaseConfig

from .base import DatabaseConnection
from .firestore import FirestoreConnection
from .mysql import MySQLConnection
from .sqlite import SQLiteConnection


class DatabaseFactory:
    """設定に基づいてデータベース接続を作成するファクトリ"""

    @staticmethod
    def create_connection(config: DatabaseConfig) -> DatabaseConnection:
        """設定に基づいてデータベース接続を作成する"""

        if config.db_type == config.SQLITE:
            db_path = config.sqlite_path or DatabaseConfig.DEFAULT_SQLITE_PATH
            return SQLiteConnection(db_path)

        elif config.db_type == config.MYSQL:
            host = config.mysql_host or DatabaseConfig.DEFAULT_MYSQL_HOST
            port = config.mysql_port or DatabaseConfig.DEFAULT_MYSQL_PORT
            user = config.mysql_user or DatabaseConfig.DEFAULT_MYSQL_USER
            password = (
                config.mysql_password
                if config.mysql_password is not None
                else DatabaseConfig.DEFAULT_MYSQL_PASSWORD
            )
            database = config.mysql_database or DatabaseConfig.DEFAULT_MYSQL_DATABASE
            return MySQLConnection(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
            )

        elif config.db_type == config.FIRESTORE:
            if not config.firestore_project_id:
                raise ValueError("Firestore project ID must be provided")
            return FirestoreConnection(
                project_id=config.firestore_project_id,
                credentials_path=config.firestore_credentials_path,
            )

        else:
            raise ValueError(f"Unsupported database type: {config.db_type}")

from typing import Optional
from app.config.database_config import DatabaseConfig
from .base import DatabaseConnection
from .sqlite import SQLiteConnection
from .mysql import MySQLConnection
from .firestore import FirestoreConnection


class DatabaseFactory:
    """設定に基づいてデータベース接続を作成するファクトリ"""

    @staticmethod
    def create_connection(config: DatabaseConfig) -> DatabaseConnection:
        """設定に基づいてデータベース接続を作成する"""

        if config.db_type == config.SQLITE:
            return SQLiteConnection(config.sqlite_path)

        elif config.db_type == config.MYSQL:
            return MySQLConnection(
                host=config.mysql_host,
                port=config.mysql_port,
                user=config.mysql_user,
                password=config.mysql_password,
                database=config.mysql_database
            )

        elif config.db_type == config.FIRESTORE:
            return FirestoreConnection(
                project_id=config.firestore_project_id,
                credentials_path=config.firestore_credentials_path
            )

        else:
            raise ValueError(f"Unsupported database type: {config.db_type}")

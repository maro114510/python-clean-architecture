from app.datastore.database.sqlite_transaction_manager import SQLiteTransactionManager
from app.datastore.database.mysql_transaction_manager import MySQLTransactionManager
from app.datastore.database.firestore_transaction_manager import (
    FirestoreTransactionManager,
)
from app.config.database_config import DatabaseConfig


class TransactionManagerFactory:
    @staticmethod
    def create_manager(connection, config: DatabaseConfig):
        if config.db_type == config.SQLITE:
            return SQLiteTransactionManager(connection)
        elif config.db_type == config.MYSQL:
            return MySQLTransactionManager(connection)
        elif config.db_type == config.FIRESTORE:
            return FirestoreTransactionManager(connection)
        else:
            raise ValueError(f"Unsupported database type: {config.db_type}")

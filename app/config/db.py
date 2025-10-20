from app.config.database_config import DatabaseConfig
from app.datastore.database import DatabaseFactory


class DB:
    """
    Database class for managing database connections.
    """

    def __init__(self):
        """Initialize the database connection using environment configurations."""
        self.config = DatabaseConfig.from_env()
        self.connection = DatabaseFactory.create_connection(self.config)

    async def get_connection(self):
        """Get the database connection."""
        return await self.connection.connect()

    async def close_connection(self):
        """Close the database connection."""
        await self.connection.disconnect()

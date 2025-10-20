import aiomysql
from typing import Dict, Any
from .base import DatabaseConnection


class MySQLConnection(DatabaseConnection):
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self._connection = None

    async def connect(self):
        self._connection = await aiomysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.database,
        )
        return self._connection

    async def disconnect(self):
        if self._connection:
            self._connection.close()
            await self._connection.wait_closed()
            self._connection = None

    def get_connection_info(self) -> Dict[str, Any]:
        return {
            "type": "mysql",
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "database": self.database,
        }

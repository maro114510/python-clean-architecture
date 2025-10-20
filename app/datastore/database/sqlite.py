import aiosqlite
from typing import Dict, Any
from .base import DatabaseConnection


class SQLiteConnection(DatabaseConnection):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._connection = None

    async def connect(self):
        if self._connection is None:
            self._connection = await aiosqlite.connect(self.db_path)
        return self._connection

    async def disconnect(self):
        if self._connection:
            await self._connection.close()
            # aiosqlite closes connections asynchronously; if supported, wait for the worker thread
            wait_closed = getattr(self._connection, "wait_closed", None)
            if callable(wait_closed):
                await wait_closed()
            self._connection = None

    def get_connection_info(self) -> Dict[str, Any]:
        return {"type": "sqlite", "db_path": self.db_path}

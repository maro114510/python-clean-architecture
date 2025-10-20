from typing import Any, Dict, List, Optional
from .transaction_manager import TransactionManager


class SQLiteTransactionManager(TransactionManager):
    async def begin(self) -> None:
        if not self._connection_obj:
            self._connection_obj = await self.connection.connect()
        self._transaction_active = True

    async def commit(self) -> None:
        if self._connection_obj and self._transaction_active:
            await self._connection_obj.commit()
            self._transaction_active = False

    async def rollback(self) -> None:
        if self._connection_obj and self._transaction_active:
            await self._connection_obj.rollback()
            self._transaction_active = False

    async def execute(
        self, sql: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        if not self._connection_obj:
            self._connection_obj = await self.connection.connect()

        cursor = await self._connection_obj.execute(sql, params or {})

        # Return query results for SELECT statements
        if sql.strip().upper().startswith("SELECT"):
            rows = await cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        else:
            # Return affected row count for INSERT/UPDATE/DELETE
            if not self._transaction_active:
                await self._connection_obj.commit()
            return [{"affected_rows": cursor.rowcount}]

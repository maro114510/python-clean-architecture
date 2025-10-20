import aiomysql
from typing import Any, Dict, List, Optional
from .transaction_manager import TransactionManager


class MySQLTransactionManager(TransactionManager):
    async def begin(self) -> None:
        if not self._connection_obj:
            self._connection_obj = await self.connection.connect()
        await self._connection_obj.begin()
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

        cursor = self._connection_obj.cursor(aiomysql.DictCursor)
        await cursor.execute(sql, params or {})

        # Return query results for SELECT statements
        if sql.strip().upper().startswith("SELECT"):
            rows = await cursor.fetchall()
            await cursor.close()
            return rows
        else:
            # Return affected row count for INSERT/UPDATE/DELETE
            affected_rows = cursor.rowcount
            await cursor.close()
            if not self._transaction_active:
                await self._connection_obj.commit()
            return [{"affected_rows": affected_rows}]

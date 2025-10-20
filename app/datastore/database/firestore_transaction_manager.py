from typing import Any, Dict, List, Optional
from .transaction_manager import TransactionManager


class FirestoreTransactionManager(TransactionManager):
    async def begin(self) -> None:
        if not self._connection_obj:
            self._connection_obj = await self.connection.connect()
        self._transaction_active = True

    async def commit(self) -> None:
        if self._connection_obj and self._transaction_active:
            # Firestore doesn't need explicit commit for transactions
            self._transaction_active = False

    async def rollback(self) -> None:
        if self._connection_obj and self._transaction_active:
            # Firestore doesn't support rollback, just mark as inactive
            self._transaction_active = False

    async def execute(
        self, sql: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError(
            "Firestore does not support SQL-based operations. "
            "SQL execution is not implemented for Firestore. "
            "Please use a SQL-compatible database (SQLite or MySQL) or implement "
            f"Firestore-specific query methods. Attempted SQL: {sql}"
        )

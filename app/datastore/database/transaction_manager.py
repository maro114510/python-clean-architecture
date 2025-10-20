from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .base import DatabaseConnection


class TransactionManager(ABC):
    """Base class for managing database transactions asynchronously."""

    def __init__(self, connection: DatabaseConnection):
        self.connection = connection
        self._connection_obj = None
        self._transaction_active = False

    @abstractmethod
    async def begin(self) -> None:
        """Initiate a new transaction"""
        pass

    @abstractmethod
    async def commit(self) -> None:
        """Commit the current transaction"""
        pass

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the current transaction"""
        pass

    @abstractmethod
    async def execute(
        self, sql: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Execute a SQL statement within the transaction context"""
        pass

    @property
    def is_transaction_active(self) -> bool:
        """Check if a transaction is currently active"""
        return self._transaction_active

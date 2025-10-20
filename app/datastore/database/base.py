from abc import ABC, abstractmethod
from typing import Any, Dict


class DatabaseConnection(ABC):
    """DB base definition class"""

    @abstractmethod
    async def connect(self) -> Any:
        """Connect to the database"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the database"""
        pass

    @abstractmethod
    def get_connection_info(self) -> Dict[str, Any]:
        """Get database connection information"""
        pass

from typing import Protocol, Any, Dict, List, Optional


class ConnectionProtocol(Protocol):
    """Protocol for database connections.

    This protocol defines the interface that all connection objects must implement.
    It uses structural subtyping (duck typing) to ensure type safety without
    requiring explicit inheritance.
    """

    async def execute(
        self, sql: str, params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Execute a SQL statement within the transaction context.

        Args:
            sql: SQL query string
            params: Optional dictionary of parameters for the query

        Returns:
            List of dictionaries representing query results or affected rows
        """
        ...

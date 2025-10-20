from abc import ABC, abstractmethod
from typing import List, Optional

from app.model.item import ItemModel


class ItemUsecase(ABC):
    @abstractmethod
    async def get_items(self) -> List[ItemModel]:
        """Retrieve all items."""

    @abstractmethod
    async def get_item(self, item_id: int) -> Optional[ItemModel]:
        """Retrieve a single item by identifier."""

    @abstractmethod
    async def create_item(self, item: ItemModel) -> None:
        """Create a new item."""

    @abstractmethod
    async def update_item(self, item_id: int, item: ItemModel) -> None:
        """Update an existing item."""

    @abstractmethod
    async def delete_item(self, item_id: int) -> None:
        """Delete an item."""

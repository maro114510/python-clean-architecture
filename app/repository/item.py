from abc import ABC, abstractmethod
from typing import List, Optional
from app.model.item import ItemModel
from app.datastore.database.connection_protocol import ConnectionProtocol


class ItemRepository(ABC):
    @abstractmethod
    async def get_items(self, connection: ConnectionProtocol) -> List[ItemModel]:
        pass

    @abstractmethod
    async def get_item(
        self, item_id: int, connection: ConnectionProtocol
    ) -> Optional[ItemModel]:
        pass

    @abstractmethod
    async def create_item(
        self, item: ItemModel, connection: ConnectionProtocol
    ) -> None:
        pass

    @abstractmethod
    async def update_item(
        self, item_id: int, item: ItemModel, connection: ConnectionProtocol
    ) -> None:
        pass

    @abstractmethod
    async def delete_item(self, item_id: int, connection: ConnectionProtocol) -> None:
        pass

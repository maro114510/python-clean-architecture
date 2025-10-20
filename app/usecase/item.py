from abc import ABC, abstractmethod
from typing import List
from app.model.item import ItemModel


class ItemUsecase(ABC):
    @abstractmethod
    def get_items(self) -> List[ItemModel]:
        pass

    @abstractmethod
    def get_item(self, item_id: int) -> ItemModel:
        pass

    @abstractmethod
    def create_item(self, item: ItemModel):
        pass

    @abstractmethod
    def update_item(self, item_id: int, item: ItemModel):
        pass

    @abstractmethod
    def delete_item(self, item_id: int):
        pass

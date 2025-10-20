from app.usecase.item import ItemUsecase
from app.repository.item import ItemRepository
from typing import List
from app.model.item import ItemModel


class ItemInteractor(ItemUsecase):
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    def get_items(self) -> List[ItemModel]:
        items = self.repo.get_items()
        return items

    def get_item(self, item_id: int) -> ItemModel:
        item = self.repo.get_item(item_id)
        return item

    def create_item(self, item) -> None:
        self.repo.create_item(item)
        return None

    def update_item(self, item_id: int, item: ItemModel) -> None:
        self.repo.update_item(item_id, item)
        return None

    def delete_item(self, item_id: int):
        self.repo.delete_item(item_id)
        return None

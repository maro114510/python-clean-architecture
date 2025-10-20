from typing import List
from app.model.item import ItemModel
from app.repository.item import ItemRepository


class ItemDatastore(ItemRepository):
    def get_items(self) -> List[ItemModel]:
        return [
            ItemModel(id=1, name="Sample Item", price=100.0),
            ItemModel(id=2, name="Another Item", price=150.0),
        ]

    def get_item(self, item_id: int) -> ItemModel:
        return ItemModel(id=item_id, name="Sample Item", price=100.0)

    def create_item(self, item) -> None:
        pass

    def update_item(self, item_id: int, item: ItemModel) -> None:
        pass

    def delete_item(self, item_id: int):
        pass

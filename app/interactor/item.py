from app.usecase.item import ItemUsecase
from app.repository.item import ItemRepository
from app.datastore.database.transaction_manager import TransactionManager
from typing import List
from app.model.item import ItemModel


class ItemInteractor(ItemUsecase):
    def __init__(self, repo: ItemRepository, transaction_manager: TransactionManager):
        self.repo = repo
        self.transaction_manager = transaction_manager

    async def get_items(self) -> List[ItemModel]:
        """Get all items"""
        try:
            await self.transaction_manager.begin()
            items = await self.repo.get_items(self.transaction_manager)
            await self.transaction_manager.commit()
            return items
        except Exception:
            await self.transaction_manager.rollback()
            raise

    async def get_item(self, item_id: int) -> ItemModel:
        """Get item by ID"""
        try:
            await self.transaction_manager.begin()
            item = await self.repo.get_item(item_id, self.transaction_manager)
            await self.transaction_manager.commit()
            return item
        except Exception:
            await self.transaction_manager.rollback()
            raise

    async def create_item(self, item: ItemModel) -> None:
        """Create a new item"""
        try:
            await self.transaction_manager.begin()
            await self.repo.create_item(item, self.transaction_manager)
            await self.transaction_manager.commit()
        except Exception:
            await self.transaction_manager.rollback()
            raise

    async def update_item(self, item_id: int, item: ItemModel) -> None:
        """Update an existing item"""
        transaction_manager = await self._get_transaction_manager()
        try:
            await self.transaction_manager.begin()
            await self.repo.update_item(item_id, item, transaction_manager)
            await self.transaction_manager.commit()
        except Exception:
            await self.transaction_manager.rollback()
            raise

    async def delete_item(self, item_id: int) -> None:
        """Delete an item by ID"""
        try:
            await self.transaction_manager.begin()
            await self.repo.delete_item(item_id, self.transaction_manager)
            await self.transaction_manager.commit()
        except Exception:
            await self.transaction_manager.rollback()
            raise

    async def _get_transaction_manager(self) -> TransactionManager:
        """Get transaction manager for database operations."""
        return self.transaction_manager

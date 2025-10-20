from typing import List, Optional
import logging
from app.model.item import ItemModel
from app.repository.item import ItemRepository
from app.datastore.database.connection_protocol import ConnectionProtocol


class ItemDatastore(ItemRepository):
    async def get_items(self, connection: ConnectionProtocol) -> List[ItemModel]:
        """Get all items"""
        sql = "SELECT * FROM item"
        try:
            rows = await connection.execute(sql)
        except Exception as e:
            logging.error(f"Error executing SQL: {sql} - {e}")
            return []

        return [ItemModel(**row) for row in rows]

    async def get_item(
        self, item_id: int, connection: ConnectionProtocol
    ) -> Optional[ItemModel]:
        """Get item by ID"""
        sql = "SELECT * FROM item WHERE id = :id"
        try:
            rows = await connection.execute(sql, {"id": item_id})
        except Exception as e:
            logging.error(f"Error executing SQL: {sql} with id={item_id} - {e}")
            return None

        return ItemModel(**rows[0]) if rows else None

    async def create_item(
        self, item: ItemModel, connection: ConnectionProtocol
    ) -> None:
        """Create a new item"""
        sql = "INSERT INTO item (name, price) VALUES (:name, :price)"
        try:
            await connection.execute(sql, {"name": item.name, "price": item.price})
        except Exception as e:
            logging.error(f"Error executing SQL: {sql} with item={item} - {e}")
            raise

    async def update_item(
        self, item_id: int, item: ItemModel, connection: ConnectionProtocol
    ) -> None:
        """Update an existing item"""
        sql = "UPDATE item SET name = :name, price = :price WHERE id = :id"
        try:
            await connection.execute(
                sql, {"name": item.name, "price": item.price, "id": item_id}
            )
        except Exception as e:
            logging.error(
                f"Error executing SQL: {sql} with id={item_id}, item={item} - {e}"
            )
            raise

    async def delete_item(self, item_id: int, connection: ConnectionProtocol) -> None:
        """Delete an item by ID"""
        sql = "DELETE FROM item WHERE id = :id"
        try:
            await connection.execute(sql, {"id": item_id})
        except Exception as e:
            logging.error(f"Error executing SQL: {sql} with id={item_id} - {e}")
            raise

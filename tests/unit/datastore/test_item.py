"""
Unit tests for ItemDatastore layer.

Tests the data access layer (ItemDatastore) with real database connections.
This layer handles SQL execution and model conversion.

Test Strategy:
- Use real database connections (SQLite, MySQL, or Firestore based on DB_TYPE env var)
- Test each CRUD method independently
- Verify SQL execution and error handling
- Test model conversion from database rows to ItemModel
- Each test is isolated with automatic rollback after execution
"""

import pytest
from app.datastore.item import ItemDatastore
from app.model.item import ItemModel


pytestmark = pytest.mark.unit


class TestItemDatastoreGetItems:
    """Test suite for ItemDatastore.get_items() method."""

    @pytest.mark.asyncio
    async def test_get_items_success(self, test_transaction, setup_test_db):
        """
        Test successful retrieval of all items.

        Arrange:
            - Insert test items into database
            - Create ItemDatastore instance

        Act:
            - Call get_items()

        Assert:
            - Returns list of ItemModel instances
            - Correct number of items returned
        """
        # Arrange - insert test data
        await test_transaction.execute(
            "INSERT INTO item (name, price) VALUES (:name, :price)",
            {"name": "Item 1", "price": 100.0},
        )
        await test_transaction.execute(
            "INSERT INTO item (name, price) VALUES (:name, :price)",
            {"name": "Item 2", "price": 200.0},
        )
        await test_transaction.execute(
            "INSERT INTO item (name, price) VALUES (:name, :price)",
            {"name": "Item 3", "price": 300.0},
        )

        datastore = ItemDatastore()

        # Act
        result = await datastore.get_items(test_transaction)

        # Assert
        assert len(result) == 3
        assert all(isinstance(item, ItemModel) for item in result)
        assert result[0].name == "Item 1"
        assert result[0].price == 100.0
        assert result[1].name == "Item 2"
        assert result[1].price == 200.0
        assert result[2].name == "Item 3"
        assert result[2].price == 300.0

    @pytest.mark.asyncio
    async def test_get_items_empty(self, test_transaction, setup_test_db):
        """
        Test retrieval when no items exist.

        Arrange:
            - Database is empty (no items inserted)

        Act:
            - Call get_items()

        Assert:
            - Returns empty list
        """
        # Arrange
        datastore = ItemDatastore()

        # Act
        result = await datastore.get_items(test_transaction)

        # Assert
        assert result == []

    @pytest.mark.asyncio
    async def test_get_items_handles_connection_error(
        self, test_transaction, setup_test_db
    ):
        """
        Test error handling when database connection fails.

        Note: This test simulates error handling by using invalid SQL
        in a way that the datastore should catch and handle gracefully.
        """

        # Create a mock connection that raises an error
        class FailingConnection:
            async def execute(self, sql, params=None):
                raise Exception("Database connection failed")

        datastore = ItemDatastore()

        # Act
        result = await datastore.get_items(FailingConnection())

        # Assert
        assert result == []


class TestItemDatastoreGetItem:
    """Test suite for ItemDatastore.get_item() method."""

    @pytest.mark.asyncio
    async def test_get_item_success(self, test_transaction, setup_test_db):
        """
        Test successful retrieval of a single item by ID.

        Arrange:
            - Insert a test item into database
            - Create ItemDatastore instance

        Act:
            - Call get_item()

        Assert:
            - Returns ItemModel instance
            - Correct item data returned
        """
        # Arrange - insert test data
        await test_transaction.execute(
            "INSERT INTO item (name, price) VALUES (:name, :price)",
            {"name": "Test Item", "price": 150.0},
        )

        datastore = ItemDatastore()

        # Act
        result = await datastore.get_item(1, test_transaction)

        # Assert
        assert isinstance(result, ItemModel)
        assert result.id == 1
        assert result.name == "Test Item"
        assert result.price == 150.0

    @pytest.mark.asyncio
    async def test_get_item_not_found(self, test_transaction, setup_test_db):
        """
        Test retrieval when item does not exist.

        Arrange:
            - No items in database

        Act:
            - Call get_item() with non-existent ID

        Assert:
            - Returns None
        """
        # Arrange
        datastore = ItemDatastore()

        # Act
        result = await datastore.get_item(999, test_transaction)

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_get_item_handles_error(self, test_transaction, setup_test_db):
        """
        Test error handling during item retrieval.

        Arrange:
            - Mock connection that raises an exception

        Act:
            - Call get_item()

        Assert:
            - Returns None and error is handled
        """

        # Create a mock connection that raises an error
        class FailingConnection:
            async def execute(self, sql, params=None):
                raise Exception("Database error")

        datastore = ItemDatastore()

        # Act
        result = await datastore.get_item(1, FailingConnection())

        # Assert
        assert result is None


class TestItemDatastoreCreateItem:
    """Test suite for ItemDatastore.create_item() method."""

    @pytest.mark.asyncio
    async def test_create_item_success(self, test_transaction, setup_test_db):
        """
        Test successful creation of a new item.

        Arrange:
            - Create ItemModel instance
            - Create ItemDatastore instance

        Act:
            - Call create_item()

        Assert:
            - Item is inserted into database
            - No exception raised
        """
        # Arrange
        # Create item without id (id is generated by database)
        item = ItemModel(id=0, name="New Item", price=99.99)
        datastore = ItemDatastore()

        # Act
        await datastore.create_item(item, test_transaction)

        # Assert - verify item was inserted
        result = await test_transaction.execute("SELECT * FROM item")
        assert len(result) == 1
        assert result[0]["name"] == "New Item"
        assert result[0]["price"] == 99.99

    @pytest.mark.asyncio
    async def test_create_item_handles_error(self, test_transaction, setup_test_db):
        """
        Test error handling during item creation.

        Arrange:
            - Mock connection that raises an exception

        Act:
            - Call create_item()

        Assert:
            - Exception is re-raised
        """
        # Arrange
        item = ItemModel(id=0, name="Test Item", price=100.0)

        class FailingConnection:
            async def execute(self, sql, params=None):
                raise Exception("Duplicate key error")

        datastore = ItemDatastore()

        # Act & Assert
        with pytest.raises(Exception, match="Duplicate key error"):
            await datastore.create_item(item, FailingConnection())


class TestItemDatastoreUpdateItem:
    """Test suite for ItemDatastore.update_item() method."""

    @pytest.mark.asyncio
    async def test_update_item_success(self, test_transaction, setup_test_db):
        """
        Test successful update of an existing item.

        Arrange:
            - Insert a test item
            - Create updated ItemModel
            - Create ItemDatastore instance

        Act:
            - Call update_item()

        Assert:
            - Item is updated in database
            - Updated values are correct
        """
        # Arrange - insert initial item
        await test_transaction.execute(
            "INSERT INTO item (name, price) VALUES (:name, :price)",
            {"name": "Original Item", "price": 100.0},
        )

        updated_item = ItemModel(id=1, name="Updated Item", price=200.0)
        datastore = ItemDatastore()

        # Act
        await datastore.update_item(1, updated_item, test_transaction)

        # Assert - verify item was updated
        result = await test_transaction.execute(
            "SELECT * FROM item WHERE id = :id", {"id": 1}
        )
        assert len(result) == 1
        assert result[0]["name"] == "Updated Item"
        assert result[0]["price"] == 200.0

    @pytest.mark.asyncio
    async def test_update_item_handles_error(self, test_transaction, setup_test_db):
        """
        Test error handling during item update.

        Arrange:
            - Mock connection that raises an exception

        Act:
            - Call update_item()

        Assert:
            - Exception is re-raised
        """
        # Arrange
        item = ItemModel(id=1, name="Test Item", price=100.0)

        class FailingConnection:
            async def execute(self, sql, params=None):
                raise Exception("Update failed")

        datastore = ItemDatastore()

        # Act & Assert
        with pytest.raises(Exception, match="Update failed"):
            await datastore.update_item(1, item, FailingConnection())


class TestItemDatastoreDeleteItem:
    """Test suite for ItemDatastore.delete_item() method."""

    @pytest.mark.asyncio
    async def test_delete_item_success(self, test_transaction, setup_test_db):
        """
        Test successful deletion of an item.

        Arrange:
            - Insert a test item
            - Create ItemDatastore instance

        Act:
            - Call delete_item()

        Assert:
            - Item is deleted from database
        """
        # Arrange - insert test item
        await test_transaction.execute(
            "INSERT INTO item (name, price) VALUES (:name, :price)",
            {"name": "Item to Delete", "price": 50.0},
        )

        datastore = ItemDatastore()

        # Act
        await datastore.delete_item(1, test_transaction)

        # Assert - verify item was deleted
        result = await test_transaction.execute(
            "SELECT * FROM item WHERE id = :id", {"id": 1}
        )
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_delete_item_handles_error(self, test_transaction, setup_test_db):
        """
        Test error handling during item deletion.

        Arrange:
            - Mock connection that raises an exception

        Act:
            - Call delete_item()

        Assert:
            - Exception is re-raised
        """

        # Arrange
        class FailingConnection:
            async def execute(self, sql, params=None):
                raise Exception("Delete failed")

        datastore = ItemDatastore()

        # Act & Assert
        with pytest.raises(Exception, match="Delete failed"):
            await datastore.delete_item(1, FailingConnection())


class TestItemDatastoreIntegration:
    """Integration tests for ItemDatastore with multiple operations."""

    @pytest.mark.asyncio
    async def test_crud_flow(self, test_transaction, setup_test_db):
        """
        Test complete CRUD flow with real database.

        Arrange:
            - Prepare datastore

        Act:
            - Execute create, read, update, delete operations

        Assert:
            - All operations complete successfully
            - Data persists and updates correctly
        """
        # Arrange
        datastore = ItemDatastore()

        # Act & Assert - Create
        created_item = ItemModel(id=0, name="New Item", price=150.0)
        await datastore.create_item(created_item, test_transaction)
        result = await datastore.get_items(test_transaction)
        assert len(result) == 1
        assert result[0].name == "New Item"

        # Act & Assert - Read
        item = await datastore.get_item(1, test_transaction)
        assert item is not None
        assert item.name == "New Item"
        assert item.price == 150.0

        # Act & Assert - Update
        updated_item = ItemModel(id=1, name="Updated Item", price=250.0)
        await datastore.update_item(1, updated_item, test_transaction)
        updated = await datastore.get_item(1, test_transaction)
        assert updated.name == "Updated Item"
        assert updated.price == 250.0

        # Act & Assert - Delete
        await datastore.delete_item(1, test_transaction)
        deleted = await datastore.get_item(1, test_transaction)
        assert deleted is None

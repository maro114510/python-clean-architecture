"""
Unit tests for ItemInteractor layer.

Tests the business logic layer with mocked repository dependencies.
This layer handles transaction management and orchestration.

Test Strategy:
- Mock ItemRepository using create_autospec (type-safe)
- Mock TransactionManager using create_autospec
- Verify repository method calls with correct arguments
- Verify transaction lifecycle (begin/commit/rollback)
- Use DeepDiff for complex object comparisons
"""

import pytest
from deepdiff import DeepDiff

from app.interactor.item import ItemInteractor
from app.repository.item import ItemRepository
from app.datastore.database.transaction_manager import TransactionManager
from app.model.item import ItemModel


pytestmark = pytest.mark.unit


class TestItemInteractorGetItems:
    """Test suite for ItemInteractor.get_items() method."""

    @pytest.mark.asyncio
    async def test_get_items_success(self, mocker):
        """Test successful retrieval with transaction management."""
        # Arrange
        mock_repo = mocker.create_autospec(ItemRepository, instance=True)
        mock_tx = mocker.create_autospec(TransactionManager, instance=True)

        expected_items = [
            ItemModel(id=1, name="Item 1", price=100.0),
            ItemModel(id=2, name="Item 2", price=200.0),
        ]
        mock_repo.get_items = mocker.AsyncMock(return_value=expected_items)

        interactor = ItemInteractor(mock_repo, mock_tx)

        # Act
        result = await interactor.get_items()

        # Assert - Repository calls with correct arguments
        mock_repo.get_items.assert_called_once_with(mock_tx)

        # Assert - Transaction lifecycle
        mock_tx.begin.assert_called_once()
        mock_tx.commit.assert_called_once()
        mock_tx.rollback.assert_not_called()

        # Assert - Result comparison using DeepDiff
        diff = DeepDiff(expected_items, result)
        assert not diff, f"Unexpected difference:\n{diff.pretty()}"

    @pytest.mark.asyncio
    async def test_get_items_rollback_on_error(self, mocker):
        """Test rollback when repository raises exception."""
        # Arrange
        mock_repo = mocker.create_autospec(ItemRepository, instance=True)
        mock_tx = mocker.create_autospec(TransactionManager, instance=True)

        mock_repo.get_items = mocker.AsyncMock(side_effect=Exception("DB Error"))

        interactor = ItemInteractor(mock_repo, mock_tx)

        # Act & Assert
        with pytest.raises(Exception, match="DB Error"):
            await interactor.get_items()

        # Assert - Rollback called on error
        mock_tx.begin.assert_called_once()
        mock_tx.rollback.assert_called_once()
        mock_tx.commit.assert_not_called()


class TestItemInteractorGetItem:
    """Test suite for ItemInteractor.get_item() method."""

    @pytest.mark.asyncio
    async def test_get_item_success(self, mocker):
        """Test successful retrieval of single item."""
        # Arrange
        mock_repo = mocker.create_autospec(ItemRepository, instance=True)
        mock_tx = mocker.create_autospec(TransactionManager, instance=True)

        expected_item = ItemModel(id=1, name="Test Item", price=150.0)
        mock_repo.get_item = mocker.AsyncMock(return_value=expected_item)

        interactor = ItemInteractor(mock_repo, mock_tx)

        # Act
        result = await interactor.get_item(1)

        # Assert - Repository called with correct arguments
        mock_repo.get_item.assert_called_once_with(1, mock_tx)

        # Assert - Transaction lifecycle
        mock_tx.begin.assert_called_once()
        mock_tx.commit.assert_called_once()

        # Assert - Result comparison
        diff = DeepDiff(expected_item, result)
        assert not diff, f"Unexpected difference:\n{diff.pretty()}"

    @pytest.mark.asyncio
    async def test_get_item_not_found(self, mocker):
        """Test retrieval when item does not exist."""
        # Arrange
        mock_repo = mocker.create_autospec(ItemRepository, instance=True)
        mock_tx = mocker.create_autospec(TransactionManager, instance=True)

        mock_repo.get_item = mocker.AsyncMock(return_value=None)

        interactor = ItemInteractor(mock_repo, mock_tx)

        # Act
        result = await interactor.get_item(999)

        # Assert
        mock_repo.get_item.assert_called_once_with(999, mock_tx)
        mock_tx.commit.assert_called_once()
        assert result is None

    @pytest.mark.asyncio
    async def test_get_item_rollback_on_error(self, mocker):
        """Test rollback when repository raises exception."""
        # Arrange
        mock_repo = mocker.create_autospec(ItemRepository, instance=True)
        mock_tx = mocker.create_autospec(TransactionManager, instance=True)

        mock_repo.get_item = mocker.AsyncMock(side_effect=Exception("DB Error"))

        interactor = ItemInteractor(mock_repo, mock_tx)

        # Act & Assert
        with pytest.raises(Exception, match="DB Error"):
            await interactor.get_item(1)

        # Assert - Rollback called on error
        mock_tx.rollback.assert_called_once()
        mock_tx.commit.assert_not_called()


class TestItemInteractorCreateItem:
    """Test suite for ItemInteractor.create_item() method."""

    @pytest.mark.asyncio
    async def test_create_item_success(self, mocker):
        """Test successful creation with correct arguments."""
        # Arrange
        mock_repo = mocker.create_autospec(ItemRepository, instance=True)
        mock_tx = mocker.create_autospec(TransactionManager, instance=True)

        mock_repo.create_item = mocker.AsyncMock()

        interactor = ItemInteractor(mock_repo, mock_tx)
        item = ItemModel(id=0, name="New Item", price=99.99)

        # Act
        await interactor.create_item(item)

        # Assert - Repository called with correct arguments
        mock_repo.create_item.assert_called_once_with(item, mock_tx)

        # Assert - Transaction lifecycle
        mock_tx.begin.assert_called_once()
        mock_tx.commit.assert_called_once()
        mock_tx.rollback.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_item_rollback_on_error(self, mocker):
        """Test rollback when creation fails."""
        # Arrange
        mock_repo = mocker.create_autospec(ItemRepository, instance=True)
        mock_tx = mocker.create_autospec(TransactionManager, instance=True)

        mock_repo.create_item = mocker.AsyncMock(side_effect=Exception("DB Error"))

        interactor = ItemInteractor(mock_repo, mock_tx)
        item = ItemModel(id=0, name="Test Item", price=100.0)

        # Act & Assert
        with pytest.raises(Exception, match="DB Error"):
            await interactor.create_item(item)

        # Assert - Rollback called
        mock_tx.rollback.assert_called_once()
        mock_tx.commit.assert_not_called()


class TestItemInteractorUpdateItem:
    """Test suite for ItemInteractor.update_item() method."""

    @pytest.mark.asyncio
    async def test_update_item_success(self, mocker):
        """Test successful update with correct arguments."""
        # Arrange
        mock_repo = mocker.create_autospec(ItemRepository, instance=True)
        mock_tx = mocker.create_autospec(TransactionManager, instance=True)

        mock_repo.update_item = mocker.AsyncMock()

        interactor = ItemInteractor(mock_repo, mock_tx)
        item = ItemModel(id=1, name="Updated Item", price=200.0)

        # Act
        await interactor.update_item(1, item)

        # Assert - Repository called with correct arguments
        mock_repo.update_item.assert_called_once_with(1, item, mock_tx)

        # Assert - Transaction lifecycle
        mock_tx.begin.assert_called_once()
        mock_tx.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_item_rollback_on_error(self, mocker):
        """Test rollback when update fails."""
        # Arrange
        mock_repo = mocker.create_autospec(ItemRepository, instance=True)
        mock_tx = mocker.create_autospec(TransactionManager, instance=True)

        mock_repo.update_item = mocker.AsyncMock(side_effect=Exception("Update failed"))

        interactor = ItemInteractor(mock_repo, mock_tx)
        item = ItemModel(id=1, name="Test Item", price=100.0)

        # Act & Assert
        with pytest.raises(Exception, match="Update failed"):
            await interactor.update_item(1, item)

        # Assert - Rollback called
        mock_tx.rollback.assert_called_once()
        mock_tx.commit.assert_not_called()


class TestItemInteractorDeleteItem:
    """Test suite for ItemInteractor.delete_item() method."""

    @pytest.mark.asyncio
    async def test_delete_item_success(self, mocker):
        """Test successful deletion with correct arguments."""
        # Arrange
        mock_repo = mocker.create_autospec(ItemRepository, instance=True)
        mock_tx = mocker.create_autospec(TransactionManager, instance=True)

        mock_repo.delete_item = mocker.AsyncMock()

        interactor = ItemInteractor(mock_repo, mock_tx)

        # Act
        await interactor.delete_item(1)

        # Assert - Repository called with correct arguments
        mock_repo.delete_item.assert_called_once_with(1, mock_tx)

        # Assert - Transaction lifecycle
        mock_tx.begin.assert_called_once()
        mock_tx.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_item_rollback_on_error(self, mocker):
        """Test rollback when deletion fails."""
        # Arrange
        mock_repo = mocker.create_autospec(ItemRepository, instance=True)
        mock_tx = mocker.create_autospec(TransactionManager, instance=True)

        mock_repo.delete_item = mocker.AsyncMock(side_effect=Exception("Delete failed"))

        interactor = ItemInteractor(mock_repo, mock_tx)

        # Act & Assert
        with pytest.raises(Exception, match="Delete failed"):
            await interactor.delete_item(1)

        # Assert - Rollback called
        mock_tx.rollback.assert_called_once()
        mock_tx.commit.assert_not_called()

"""Unit tests for the item router.

These tests verify that the FastAPI router resolves dependencies via the
`Container` just like the interactor layer, allowing us to inject a mocked
use case and exercise the HTTP endpoints end-to-end.
"""

from http import HTTPStatus

import pytest
from dependency_injector import providers
from fastapi import FastAPI
from fastapi.testclient import TestClient
from typing import TypedDict

from app.container import Container
from app.interactor.item import ItemInteractor
from app.model.item import ItemModel
from app.router.item import router


pytestmark = pytest.mark.unit


class _ItemPayload(TypedDict):
    name: str
    price: float


@pytest.fixture
def mock_usecase(mocker):
    """Provide an ItemUsecase-like mock with async endpoints."""

    mock = mocker.create_autospec(ItemInteractor, instance=True)
    mock.get_items = mocker.AsyncMock(return_value=[])
    mock.get_item = mocker.AsyncMock(return_value=None)
    mock.create_item = mocker.AsyncMock()
    mock.update_item = mocker.AsyncMock()
    mock.delete_item = mocker.AsyncMock()
    return mock


@pytest.fixture
def client(mock_usecase):
    """Create a FastAPI TestClient with the router wired through the container."""

    container = Container()
    container.item_usecase.override(providers.Object(mock_usecase))
    container.wire(modules=["app.router.item"])

    app = FastAPI()
    app.include_router(router)

    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client

    container.unwire()
    container.item_usecase.reset_override()


class TestListItems:
    def test_list_items_success(self, client, mock_usecase):
        items = [
            ItemModel(id=1, name="First", price=10.0),
            ItemModel(id=2, name="Second", price=20.0),
        ]
        mock_usecase.get_items.return_value = items

        response = client.get("/item")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == [item.model_dump(by_alias=True) for item in items]
        mock_usecase.get_items.assert_awaited_once()

    def test_list_items_error_returns_500(self, client, mock_usecase):
        mock_usecase.get_items.side_effect = RuntimeError("boom")

        response = client.get("/item")

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        mock_usecase.get_items.assert_awaited_once()


class TestGetItem:
    def test_get_item_success(self, client, mock_usecase):
        item = ItemModel(id=1, name="Single", price=99.99)
        mock_usecase.get_item.return_value = item

        response = client.get("/item/1")

        assert response.status_code == HTTPStatus.OK
        assert response.json() == item.model_dump(by_alias=True)
        mock_usecase.get_item.assert_awaited_once_with(1)

    def test_get_item_error_returns_500(self, client, mock_usecase):
        mock_usecase.get_item.side_effect = LookupError("missing")

        response = client.get("/item/1")

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        mock_usecase.get_item.assert_awaited_once_with(1)


class TestCreateItem:
    def test_create_item_success(self, client, mock_usecase):
        payload: _ItemPayload = {"name": "Created", "price": 123.45}

        response = client.post("/item", json=payload)

        assert response.status_code == HTTPStatus.CREATED
        mock_usecase.create_item.assert_awaited_once()
        sent_item = mock_usecase.create_item.await_args.args[0]
        assert isinstance(sent_item, ItemModel)
        expected = ItemModel(name=payload["name"], price=payload["price"])
        assert sent_item.model_dump() == expected.model_dump()


class TestUpdateItem:
    def test_update_item_success(self, client, mock_usecase):
        payload: _ItemPayload = {"name": "Updated", "price": 555.0}

        response = client.put("/item/5", json=payload)

        assert response.status_code == HTTPStatus.NO_CONTENT
        mock_usecase.update_item.assert_awaited_once()
        args = mock_usecase.update_item.await_args.args
        assert args[0] == 5
        sent_item = args[1]
        assert isinstance(sent_item, ItemModel)
        expected = ItemModel(
            id=5,
            name=payload["name"],
            price=payload["price"],
        )
        assert sent_item.model_dump() == expected.model_dump()


class TestDeleteItem:
    def test_delete_item_success(self, client, mock_usecase):
        response = client.delete("/item/9")

        assert response.status_code == HTTPStatus.NO_CONTENT
        mock_usecase.delete_item.assert_awaited_once_with(9)

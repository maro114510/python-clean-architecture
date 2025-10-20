from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from app.schema.item import ItemResponse, ItemRequest
from app.usecase.item import ItemUsecase
from app.container import Container

router = APIRouter()


@router.get("/item", response_model=list[ItemResponse])
@inject
def list_items(usecase: ItemUsecase = Depends(Provide[Container.item_usecase])):
    items = usecase.get_items()
    return items


@router.get("/item/{item_id}", response_model=ItemResponse)
@inject
def get_item(
    item_id: int, usecase: ItemUsecase = Depends(Provide[Container.item_usecase])
):
    item = usecase.get_item(item_id)
    return item


@router.post("/item", response_model=None, status_code=201)
@inject
def create_item(
    item: ItemRequest, usecase: ItemUsecase = Depends(Provide[Container.item_usecase])
):
    usecase.create_item(item)
    return None


@router.put("/item/{item_id}", response_model=None, status_code=204)
@inject
def update_item(
    item_id: int,
    item: ItemRequest,
    usecase: ItemUsecase = Depends(Provide[Container.item_usecase]),
):
    usecase.update_item(item_id, item)
    return None


@router.delete("/item/{item_id}", response_model=None, status_code=204)
@inject
def delete_item(
    item_id: int, usecase: ItemUsecase = Depends(Provide[Container.item_usecase])
):
    usecase.delete_item(item_id)
    return None

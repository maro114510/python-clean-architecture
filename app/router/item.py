from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.container import Container
from app.model.item import ItemModel
from app.schema.item import ItemRequest, ItemResponse
from app.usecase.item import ItemUsecase

router = APIRouter()


@router.get("/item", response_model=list[ItemResponse])
@inject
async def list_items(usecase: ItemUsecase = Depends(Provide[Container.item_usecase])):
    try:
        items = await usecase.get_items()
        return items
    except Exception as e:
        raise e


@router.get("/item/{item_id}", response_model=ItemResponse)
@inject
async def get_item(
    item_id: int, usecase: ItemUsecase = Depends(Provide[Container.item_usecase])
):
    try:
        item = await usecase.get_item(item_id)
        return item
    except Exception as e:
        raise e


@router.post(
    "/item",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_item(
    item: ItemRequest, usecase: ItemUsecase = Depends(Provide[Container.item_usecase])
):
    try:
        domain_item = ItemModel(**item.model_dump())
        await usecase.create_item(domain_item)
        return None
    except Exception as e:
        raise e


@router.put(
    "/item/{item_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def update_item(
    item_id: int,
    item: ItemRequest,
    usecase: ItemUsecase = Depends(Provide[Container.item_usecase]),
):
    try:
        domain_item = ItemModel(id=item_id, **item.model_dump())
        await usecase.update_item(item_id, domain_item)
        return None
    except Exception as e:
        raise e


@router.delete(
    "/item/{item_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_item(
    item_id: int, usecase: ItemUsecase = Depends(Provide[Container.item_usecase])
):
    try:
        await usecase.delete_item(item_id)
        return None
    except Exception as e:
        raise e

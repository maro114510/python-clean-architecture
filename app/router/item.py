from fastapi import APIRouter
from app.schema.item import ItemResponse, ItemRequest

router = APIRouter()


@router.get("/item", response_model=list[ItemResponse])
def list_items():
    return [
        ItemResponse(id=1, name="Sample Item", price=100.0),
        ItemResponse(id=2, name="Another Item", price=150.0),
    ]


@router.get("/item/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    return ItemResponse(id=item_id, name="Sample Item", price=100.0)


@router.post("/item", response_model=None, status_code=201)
def create_item(item: ItemRequest):
    return ItemResponse(id=1, name="Sample Item", price=100.0)


@router.put("/item/{item_id}", response_model=None, status_code=204)
def update_item(item_id: int, item: ItemRequest):
    return ItemResponse(id=item_id, name="Sample Item", price=100.0)


@router.delete("/item/{item_id}", response_model=None, status_code=204)
def delete_item(item_id: int):
    return ItemResponse(id=item_id, name="Sample Item", price=100.0)

from typing import Optional
from app.schema.core import BaseSchema
from app.model.item import ItemModel


class ItemResponse(BaseSchema, ItemModel):
    pass


class ItemRequest(BaseSchema, ItemModel):
    name: Optional[str] = None
    price: Optional[float] = None

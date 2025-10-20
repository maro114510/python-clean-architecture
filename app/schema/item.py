from app.schema.core import BaseSchema
from app.model.item import ItemModel, ItemBase


class ItemResponse(BaseSchema, ItemModel):
    pass


class ItemRequest(BaseSchema, ItemBase):
    pass

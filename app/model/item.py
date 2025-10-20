from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    price: float


class ItemModel(ItemBase):
    id: int

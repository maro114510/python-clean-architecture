from pydantic import BaseModel
from humps.camel import case


class BaseSchema(BaseModel):
    model_config = {"alias_generator": case, "populate_by_name": True}

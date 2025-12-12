from typing import Union
from uuid import UUID
from pydantic import BaseModel

class IdentifiableEntity(BaseModel):
    id: Union[str, int, UUID]

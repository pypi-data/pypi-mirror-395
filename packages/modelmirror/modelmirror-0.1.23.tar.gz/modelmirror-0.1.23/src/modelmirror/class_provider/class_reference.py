from typing import Type

from pydantic import BaseModel


class ClassReference(BaseModel):
    id: str
    cls: Type

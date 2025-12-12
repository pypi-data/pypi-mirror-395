from dataclasses import dataclass
from typing import Literal

type ModelLinkType = Literal["type", "instance"]


@dataclass
class ModelLink:
    id: str
    type: ModelLinkType

    def __hash__(self) -> int:
        return hash((self.id, self.type))

from abc import ABC, abstractmethod
from typing import Any

from modelmirror.parser.model_link import ModelLink


class ModelLinkParser(ABC):
    @abstractmethod
    def parse(self, value: Any) -> ModelLink | None:
        raise NotImplementedError

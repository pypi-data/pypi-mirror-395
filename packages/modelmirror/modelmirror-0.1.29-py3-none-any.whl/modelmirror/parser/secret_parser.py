from abc import ABC, abstractmethod

from modelmirror.parser.mirror_secret import MirrorSecret


class SecretParser(ABC):
    @abstractmethod
    def parse(self, name: str) -> MirrorSecret | None:
        raise NotImplementedError

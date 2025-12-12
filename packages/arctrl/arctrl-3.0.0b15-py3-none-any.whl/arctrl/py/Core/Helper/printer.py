from abc import abstractmethod
from typing import Protocol

class IISAPrintable(Protocol):
    @abstractmethod
    def Print(self) -> str:
        ...

    @abstractmethod
    def PrintCompact(self) -> str:
        ...



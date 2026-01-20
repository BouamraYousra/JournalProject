from abc import ABC, abstractmethod


class BaseEntry(ABC):

    @abstractmethod
    def get_content(self) -> str:
        pass

    @abstractmethod
    def edit_content(self, text: str) -> None:
        pass

    @abstractmethod
    def metadata(self) -> dict:
        pass

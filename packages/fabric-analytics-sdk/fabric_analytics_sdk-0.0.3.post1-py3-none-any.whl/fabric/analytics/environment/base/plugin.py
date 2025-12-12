from abc import ABC, abstractmethod


class IPlugin(ABC):
    @abstractmethod
    def in_context(self) -> bool:
        raise Exception("Method Not Implemented")

    priority: int = 100  # smaller number means higher priority

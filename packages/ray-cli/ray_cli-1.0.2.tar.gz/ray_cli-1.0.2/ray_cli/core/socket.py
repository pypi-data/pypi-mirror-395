from abc import ABC, abstractmethod


class BaseUDPSocket(ABC):
    @abstractmethod
    def open(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def send(self, payload: bytes) -> None: ...

    def __enter__(self) -> "BaseUDPSocket":
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

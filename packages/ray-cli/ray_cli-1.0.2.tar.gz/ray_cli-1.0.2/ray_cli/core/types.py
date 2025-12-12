import ipaddress
from abc import ABC, abstractmethod
from typing import Callable, Generic, Hashable, Optional, Sequence, TypeVar

from .socket import BaseUDPSocket

FrameEncoder = Callable[[int, Sequence[int]], bytes]

U = TypeVar("U", bound=Hashable)


class ProtocolFactory(ABC, Generic[U]):
    @abstractmethod
    def create_frame_encoder(self, universe) -> FrameEncoder: ...

    @abstractmethod
    def create_socket(
        self,
        universe: U,
        src: ipaddress.IPv4Address,
        dst: Optional[ipaddress.IPv4Address],
    ) -> BaseUDPSocket: ...

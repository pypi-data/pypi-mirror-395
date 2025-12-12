import ipaddress
import itertools
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, Optional, Sequence

from .socket import BaseUDPSocket
from .types import FrameEncoder, ProtocolFactory, U


@dataclass
class Universe:
    socket: BaseUDPSocket
    encode: FrameEncoder
    seq_iter: itertools.cycle = field(
        default_factory=lambda: itertools.cycle(range(256))
    )


class BaseSender(ABC):
    @abstractmethod
    def open(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def send(self, dmx_data: Sequence[int]) -> None: ...

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()


class Sender(BaseSender, Generic[U]):
    def __init__(
        self,
        universes: Sequence[U],
        factory: ProtocolFactory,
        *,
        src: ipaddress.IPv4Address = ipaddress.IPv4Address("0.0.0.0"),
        dst: Optional[ipaddress.IPv4Address] = None,
    ):
        self._universes = {}
        for universe in universes:
            self._universes[universe] = Universe(
                socket=factory.create_socket(universe, src, dst),
                encode=factory.create_frame_encoder(universe),
            )

    def open(self) -> None:
        for universe in self._universes.values():
            universe.socket.open()

    def close(self) -> None:
        for universe in self._universes.values():
            universe.socket.close()

    def send(self, dmx_data: Sequence[int]) -> None:
        for universe in self._universes.values():
            seq = next(universe.seq_iter)
            universe.socket.send(universe.encode(seq, dmx_data))

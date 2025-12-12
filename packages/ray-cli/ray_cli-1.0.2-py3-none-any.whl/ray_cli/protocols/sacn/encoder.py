from abc import ABC, abstractmethod
from typing import Sequence

from .packets import DataPacket


class Encoder(ABC):
    @abstractmethod
    def build_frame(
        self,
        universe: int,
        priority: int,
        sequence: int,
        dmx_data: Sequence[int],
    ) -> bytes: ...


class SACNEncoder(Encoder):
    def __init__(
        self,
        cid: bytes,
        source_name: str,
    ):
        self.cid = cid
        self.source_name = source_name

    def build_frame(
        self,
        universe: int,
        priority: int,
        sequence: int,
        dmx_data: Sequence[int],
    ) -> bytes:
        return bytes(
            DataPacket(
                universe=universe,
                sequence=sequence,
                priority=priority,
                cid=self.cid,
                source_name=self.source_name,
                dmx_data=dmx_data,
            )
        )

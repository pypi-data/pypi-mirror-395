from abc import ABC, abstractmethod
from itertools import chain, islice, repeat
from typing import Sequence

from .packets import ArtDmx, ArtNetUniverse


class Encoder(ABC):
    @abstractmethod
    def build_frame(
        self,
        universe: ArtNetUniverse,
        physical: int,
        sequence: int,
        dmx_data: Sequence[int],
    ) -> bytes: ...


class ArtNetEncoder(Encoder):
    def build_frame(
        self,
        universe: ArtNetUniverse,
        physical: int,
        sequence: int,
        dmx_data: Sequence[int],
    ) -> bytes:
        return bytes(
            ArtDmx(
                sub_uni=((universe.sub_net & 0x0F) << 4) | (universe.uni & 0x0F),
                net=universe.net & 0x0F,
                physical=physical,
                sequence=sequence,
                dmx_data=list(islice(chain(dmx_data, repeat(0)), 512)),
            )
        )

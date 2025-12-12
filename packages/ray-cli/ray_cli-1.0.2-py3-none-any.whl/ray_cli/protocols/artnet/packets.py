import struct
from dataclasses import dataclass, field
from enum import Enum
from typing import Sequence

ARTNET_ID = b"Art-Net\x00"

PROT_VER = 14


class OpCode(Enum):
    ART_DMX = 0x5000


@dataclass(frozen=True, order=True)
class ArtNetUniverse:
    net: int
    sub_net: int
    uni: int

    def __bytes__(self) -> bytes:
        sub_uni = ((self.sub_net & 0x0F) << 4) | (self.uni & 0x0F)
        return bytes([sub_uni, self.net & 0x7F])

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"{self.net}.{self.sub_net}.{self.uni}"

    @staticmethod
    def from_str(string: str) -> "ArtNetUniverse":
        net, sub_net, uni = map(int, string.split("."))
        return ArtNetUniverse(net, sub_net, uni)


@dataclass
class ArtDmx:
    sub_uni: int
    net: int
    prot_ver: int = PROT_VER
    sequence: int = 0
    physical: int = 0
    dmx_data: Sequence[int] = field(default_factory=lambda: [0] * 512)

    def __bytes__(self) -> bytes:
        return (
            ARTNET_ID
            + struct.pack(
                "<H",
                OpCode.ART_DMX.value,
            )
            + struct.pack(
                ">HBBBBH",
                self.prot_ver,
                self.sequence,
                self.physical,
                self.sub_uni,
                self.net,
                len(self.dmx_data),
            )
            + bytes(self.dmx_data)
        )

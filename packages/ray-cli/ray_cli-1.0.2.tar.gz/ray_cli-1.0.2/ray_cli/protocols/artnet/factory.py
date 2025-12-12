import ipaddress
from typing import Optional, Sequence

from ray_cli.core import FrameEncoder, ProtocolFactory

from .encoder import ArtNetEncoder
from .packets import ArtNetUniverse
from .sockets import ArtNetBroadcastSocket, ArtNetUnicastSocket, BaseUDPSocket


class ArtNetFactory(ProtocolFactory[ArtNetUniverse]):
    def __init__(
        self,
        *,
        physical: int = 0,
    ):
        self._encoder = ArtNetEncoder()
        self._physical = physical

    def create_frame_encoder(self, universe: ArtNetUniverse) -> FrameEncoder:
        def build(seq: int, dmx: Sequence[int]) -> bytes:
            return self._encoder.build_frame(
                universe=universe,
                physical=self._physical,
                sequence=seq,
                dmx_data=dmx,
            )

        return build

    def create_socket(
        self,
        universe: ArtNetUniverse,
        src: ipaddress.IPv4Address,
        dst: Optional[ipaddress.IPv4Address] = None,
    ) -> BaseUDPSocket:
        return (
            ArtNetUnicastSocket(
                bind_address=src,
                dest_address=dst,
            )
            if dst is not None
            else ArtNetBroadcastSocket()
        )

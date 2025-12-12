import ipaddress
import uuid
from typing import Optional, Sequence

from ray_cli.core import FrameEncoder, ProtocolFactory

from .encoder import SACNEncoder
from .sockets import (
    BaseUDPSocket,
    SACNMulticastSocket,
    SACNUnicastSocket,
    sacn_multicast_address,
)


class SACNFactory(ProtocolFactory[int]):
    def __init__(
        self,
        *,
        source_name: str,
        priority: int = 100,
        cid: Optional[bytes] = None,
    ):
        self._priority = priority
        self._encoder = SACNEncoder(
            cid=cid or uuid.uuid4().bytes, source_name=source_name
        )

    def create_frame_encoder(
        self,
        universe: int,
    ) -> FrameEncoder:
        def build(seq: int, dmx: Sequence[int]) -> bytes:
            return self._encoder.build_frame(
                universe=universe,
                priority=self._priority,
                sequence=seq,
                dmx_data=dmx,
            )

        return build

    def create_socket(
        self,
        universe: int,
        src: ipaddress.IPv4Address,
        dst: Optional[ipaddress.IPv4Address] = None,
    ) -> BaseUDPSocket:
        return (
            SACNUnicastSocket(
                bind_address=src,
                dest_address=dst,
            )
            if dst is not None
            else SACNMulticastSocket(
                bind_address=src,
                group_address=sacn_multicast_address(universe),
            )
        )

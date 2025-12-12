import socket
from abc import abstractmethod
from ipaddress import IPv4Address
from typing import Optional

from ray_cli.core.socket import BaseUDPSocket

DEFAULT_PORT = 6454


def pick_outgoing_ip_via_route(group_address: IPv4Address):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((str(group_address), DEFAULT_PORT))
        return IPv4Address(s.getsockname()[0])

    finally:
        s.close()


class BaseArtNetUDPSocket(BaseUDPSocket):
    def __init__(
        self,
        dest_address: IPv4Address,
        bind_address: IPv4Address = IPv4Address("0.0.0.0"),
    ):
        self._dest_address = dest_address
        self._bind_address = bind_address
        self._port = DEFAULT_PORT
        self._sock: Optional[socket.socket] = None

    @abstractmethod
    def _configure_socket(self, sock: socket.socket) -> None: ...

    def open(self) -> None:
        if self._sock is not None:
            return

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except OSError:
            pass

        s.bind((str(self._bind_address), self._port))

        self._configure_socket(s)

        self._sock = s

    def close(self) -> None:
        if self._sock is not None:
            self._sock.close()
            self._sock = None

    def send(self, payload: bytes) -> None:
        if self._sock is None:
            raise RuntimeError("Socket is not open")

        self._sock.sendto(payload, (str(self._dest_address), self._port))


class ArtNetUnicastSocket(BaseArtNetUDPSocket):
    def _configure_socket(self, sock: socket.socket) -> None:
        return


class ArtNetBroadcastSocket(BaseArtNetUDPSocket):
    def __init__(self):
        super().__init__(
            dest_address=IPv4Address("255.255.255.255"),
            bind_address=IPv4Address("0.0.0.0"),
        )

    def _configure_socket(self, sock: socket.socket) -> None:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

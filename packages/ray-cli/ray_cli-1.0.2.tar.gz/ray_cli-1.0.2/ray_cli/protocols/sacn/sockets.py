import socket
from abc import abstractmethod
from ipaddress import IPv4Address
from typing import Optional

from ray_cli.core import BaseUDPSocket

DEFAULT_PORT = 5568


def sacn_multicast_address(universe: int) -> IPv4Address:
    if not 1 <= universe <= 63999:
        raise ValueError("Universe must be in range 1-63999")

    hi = (universe >> 8) & 0xFF
    lo = universe & 0xFF

    return IPv4Address(f"239.255.{hi}.{lo}")


def pick_outgoing_ip_via_route(group_address: IPv4Address):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((str(group_address), DEFAULT_PORT))
        return IPv4Address(s.getsockname()[0])

    finally:
        s.close()


class BaseSACNSocket(BaseUDPSocket):
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


class SACNUnicastSocket(BaseSACNSocket):
    def _configure_socket(self, sock: socket.socket) -> None:
        return


class SACNMulticastSocket(BaseSACNSocket):
    def __init__(
        self,
        group_address: IPv4Address,
        bind_address: IPv4Address = IPv4Address("0.0.0.0"),
        ttl: int = 1,
    ):
        super().__init__(
            dest_address=group_address,
            bind_address=bind_address,
        )
        self._ttl = ttl

    def _configure_socket(self, sock: socket.socket) -> None:
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self._ttl)

        if_ip = (
            self._bind_address
            if self._bind_address != IPv4Address("0.0.0.0")
            else pick_outgoing_ip_via_route(self._dest_address)
        )

        sock.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_MULTICAST_IF,
            socket.inet_aton(str(if_ip)),
        )

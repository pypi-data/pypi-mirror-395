import queue
import socket
import struct
import subprocess
import sys
import threading
import time
from typing import List

import pytest

from ray_cli.protocols.sacn.packets import ACN_PID

SACN_PORT = 5568

UCAST_ADDR = "127.0.0.1"
MCAST_GROUP = "239.255.0.1"
BIND_ADDR = "0.0.0.0"


def is_sacn_packet(data: bytes) -> bool:
    if not data:
        return False
    if ACN_PID not in data:
        return False
    return True


def make_unicast_socket() -> socket.socket:
    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM,
    )

    # Reuse port...
    s.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEPORT,
        1,
    )

    s.bind((UCAST_ADDR, SACN_PORT))

    return s


def make_multicast_socket() -> socket.socket:
    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM,
    )

    # Reuse port...
    s.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEPORT,
        1,
    )

    s.bind((BIND_ADDR, SACN_PORT))

    # Join multicast group on all interfaces...
    s.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        struct.pack(
            "4s4s",
            socket.inet_aton(MCAST_GROUP),
            socket.inet_aton(BIND_ADDR),
        ),
    )

    return s


@pytest.fixture(name="udp_socket")
def fixture_udp_socket(request):
    mode = getattr(request, "param", "unicast")

    if mode == "unicast":
        s = make_unicast_socket()
    elif mode == "multicast":
        s = make_multicast_socket()
    else:
        raise ValueError(f"Unknown rx_socket mode: {mode}")

    yield s

    s.close()


@pytest.fixture(name="udp_capture")
def fixture_udp_capture(udp_socket: socket.socket):
    q = queue.Queue()

    stopped = threading.Event()
    started = threading.Event()

    udp_socket.settimeout(1.0)

    def run():
        started.set()
        while not stopped.is_set():
            try:
                data, _ = udp_socket.recvfrom(4096)
                q.put(data)
            except socket.timeout:
                continue
            except OSError:
                break

    t = threading.Thread(target=run, daemon=True)
    t.start()

    started.wait(timeout=1.0)

    yield q

    stopped.set()
    t.join(timeout=1.0)


@pytest.mark.integration_tests
@pytest.mark.parametrize(
    "udp_socket, args, addr",
    [
        pytest.param(
            "unicast",
            ["--dst", UCAST_ADDR],
            f"{UCAST_ADDR}:{SACN_PORT}",
        ),
        pytest.param(
            "multicast",
            [],
            f"{MCAST_GROUP}:{SACN_PORT}",
        ),
    ],
    indirect=["udp_socket"],
)
def test_sends_udp_packet(
    args: List[str],
    addr: str,
    udp_capture: queue.Queue,
):
    p = subprocess.run(
        [sys.executable, "-m", "ray_cli", "sacn", "--packets", "1", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert p.returncode == 0, p.stderr.decode()

    packets = []
    deadline = time.monotonic() + 2.5
    while time.monotonic() < deadline:
        try:
            packets.append(udp_capture.get(timeout=0.25))
        except queue.Empty:
            continue

    assert packets, f"No sACN UDP packets received on {addr}"
    assert all(is_sacn_packet(packet) for packet in packets), "Not a sACN packet"

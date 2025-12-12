from dataclasses import dataclass, field
from typing import Sequence

ACN_PREAMBLE_SIZE = 0x0010
ACN_POSTAMBLE_SIZE = 0x0000
ACN_PID = b"ASC-E1.17\x00\x00\x00"

# Root layer vectors
VECTOR_ROOT_E131_DATA = 0x00000004

# Framing layer vectors
VECTOR_E131_DATA_PACKET = 0x00000002

# DMP vectors
VECTOR_DMP_SET_PROPERTY = 0x02


@dataclass
class DMPLayer:
    start_code: int = 0x00
    dmx_data: bytes = b""
    address_type: int = 0xA1
    first_property_address: int = 0x0000
    address_increment: int = 0x0001

    def __bytes__(self) -> bytes:
        property_values = bytes([self.start_code]) + self.dmx_data
        prop_value_count = len(property_values)

        pdu_length = 10 + prop_value_count
        flags_length = 0x7000 | pdu_length

        return (
            flags_length.to_bytes(2, "big")
            + bytes([VECTOR_DMP_SET_PROPERTY])
            + bytes([self.address_type])
            + self.first_property_address.to_bytes(2, "big")
            + self.address_increment.to_bytes(2, "big")
            + prop_value_count.to_bytes(2, "big")
            + property_values
        )


@dataclass
class FramingLayer:
    source_name: str
    universe: int
    sequence_number: int = 0
    priority: int = 100
    sync_address: int = 0
    options: int = 0
    dmp_layer: DMPLayer = field(default_factory=DMPLayer)

    def __bytes__(self) -> bytes:
        dmp_bytes = bytes(self.dmp_layer)

        pdu_length = 77 + len(dmp_bytes)
        flags_length = 0x7000 | pdu_length

        source_name_bytes = self.source_name.encode("utf-8")[:63]
        source_name_bytes = source_name_bytes.ljust(64, b"\x00")

        return (
            flags_length.to_bytes(2, "big")
            + VECTOR_E131_DATA_PACKET.to_bytes(4, "big")
            + source_name_bytes
            + bytes([self.priority])
            + self.sync_address.to_bytes(2, "big")
            + bytes([self.sequence_number])
            + bytes([self.options])
            + self.universe.to_bytes(2, "big")
            + dmp_bytes
        )


@dataclass
class RootLayer:
    cid: bytes
    vector: int
    child_pdu: bytes

    def __bytes__(self) -> bytes:
        pdu_length = 22 + len(self.child_pdu)
        flags_length = 0x7000 | pdu_length

        return (
            ACN_PREAMBLE_SIZE.to_bytes(2, "big")
            + ACN_POSTAMBLE_SIZE.to_bytes(2, "big")
            + ACN_PID
            + flags_length.to_bytes(2, "big")
            + self.vector.to_bytes(4, "big")
            + self.cid
            + self.child_pdu
        )


@dataclass
class DataPacket:
    cid: bytes
    source_name: str = ""
    universe: int = 1
    sequence: int = 0
    priority: int = 100
    dmx_data: Sequence[int] = field(default_factory=lambda: [0] * 512)

    def __bytes__(self) -> bytes:
        dmp = DMPLayer(dmx_data=bytes(self.dmx_data))

        framing = FramingLayer(
            source_name=self.source_name,
            universe=self.universe,
            sequence_number=self.sequence,
            priority=self.priority,
            dmp_layer=dmp,
        )

        framing_bytes = bytes(framing)

        root = RootLayer(
            cid=self.cid,
            vector=VECTOR_ROOT_E131_DATA,
            child_pdu=framing_bytes,
        )

        return bytes(root)

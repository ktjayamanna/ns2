from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .packetizer import PacketEvent


class TrafficClass(Enum):
    CONTROL = "control"
    BULK = "bulk"


@dataclass(frozen=True)
class ClassifiedPacketEvent:
    wave_id: int
    sender_id: int
    packet_index_for_sender: int
    packet_start_us: int
    packet_size_bytes: int
    traffic_class: TrafficClass
    priority_tag: int


def classify_packets(
    *,
    packet_events: list[PacketEvent],
    control_packet_every_n: int,
    control_priority_tag: int = 46,
    bulk_priority_tag: int = 0,
) -> list[ClassifiedPacketEvent]:
    if control_packet_every_n <= 0:
        raise ValueError("control_packet_every_n must be > 0")

    classified_events: list[ClassifiedPacketEvent] = []
    for packet_index, packet_event in enumerate(packet_events):
        is_control = packet_index % control_packet_every_n == 0
        traffic_class = TrafficClass.CONTROL if is_control else TrafficClass.BULK
        priority_tag = control_priority_tag if is_control else bulk_priority_tag

        classified_events.append(
            ClassifiedPacketEvent(
                wave_id=packet_event.wave_id,
                sender_id=packet_event.sender_id,
                packet_index_for_sender=packet_event.packet_index_for_sender,
                packet_start_us=packet_event.packet_start_us,
                packet_size_bytes=packet_event.packet_size_bytes,
                traffic_class=traffic_class,
                priority_tag=priority_tag,
            )
        )

    return classified_events

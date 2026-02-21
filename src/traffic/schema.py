from __future__ import annotations

from dataclasses import dataclass

from .models.classifier import TrafficClass


@dataclass(frozen=True)
class TrafficEvent:
    wave_id: int
    sender_id: int
    packet_index_for_sender: int
    packet_start_us: int
    packet_size_bytes: int
    traffic_class: TrafficClass
    priority_tag: int


TrafficEvents = list[TrafficEvent]

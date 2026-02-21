from __future__ import annotations

from dataclasses import dataclass

from .incast_wave import WaveStart


@dataclass(frozen=True)
class PacketEvent:
    wave_id: int
    sender_id: int
    packet_index_for_sender: int
    packet_start_us: int
    packet_size_bytes: int


def packetize_wave_starts(
    *,
    wave_starts: list[WaveStart],
    bytes_per_sender_per_wave: int,
    packet_size_bytes: int,
) -> list[PacketEvent]:
    if bytes_per_sender_per_wave < 0:
        raise ValueError("bytes_per_sender_per_wave must be >= 0")
    if packet_size_bytes <= 0:
        raise ValueError("packet_size_bytes must be > 0")
    if bytes_per_sender_per_wave == 0:
        return []

    full_packets = bytes_per_sender_per_wave // packet_size_bytes
    last_packet_remainder = bytes_per_sender_per_wave % packet_size_bytes

    packet_events: list[PacketEvent] = []
    for wave_start in wave_starts:
        packet_index_for_sender = 0

        for _ in range(full_packets):
            packet_events.append(
                PacketEvent(
                    wave_id=wave_start.wave_id,
                    sender_id=wave_start.sender_id,
                    packet_index_for_sender=packet_index_for_sender,
                    packet_start_us=wave_start.sender_start_us,
                    packet_size_bytes=packet_size_bytes,
                )
            )
            packet_index_for_sender += 1

        if last_packet_remainder > 0:
            packet_events.append(
                PacketEvent(
                    wave_id=wave_start.wave_id,
                    sender_id=wave_start.sender_id,
                    packet_index_for_sender=packet_index_for_sender,
                    packet_start_us=wave_start.sender_start_us,
                    packet_size_bytes=last_packet_remainder,
                )
            )

    return packet_events

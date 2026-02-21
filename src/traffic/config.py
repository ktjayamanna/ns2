from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class TrafficConfig:
    senders_per_wave: int
    number_of_waves: int
    first_wave_start_us: int
    wave_interval_us: int
    max_start_offset_us: int
    seed: int
    bytes_per_sender_per_wave: int
    packet_size_bytes: int
    control_packet_every_n: int
    control_priority_tag: int = 46
    bulk_priority_tag: int = 0


class ScenarioName(Enum):
    NORMAL_TRAFFIC = "normal_traffic"
    HIGH_CONGESTION = "high_congestion"
    CONGESTION_AVOIDANCE = "congestion_avoidance"

def normal_traffic() -> TrafficConfig:
    return TrafficConfig(
        senders_per_wave=32,
        number_of_waves=100,
        first_wave_start_us=0,
        wave_interval_us=5_000,
        max_start_offset_us=50,
        seed=7,
        bytes_per_sender_per_wave=128 * 1024,
        packet_size_bytes=1_500,
        control_packet_every_n=20,
    )


def high_congestion() -> TrafficConfig:
    return TrafficConfig(
        senders_per_wave=128,
        number_of_waves=150,
        first_wave_start_us=0,
        wave_interval_us=2_000,
        max_start_offset_us=20,
        seed=11,
        bytes_per_sender_per_wave=512 * 1024,
        packet_size_bytes=1_500,
        control_packet_every_n=25,
    )


def congestion_avoidance() -> TrafficConfig:
    return TrafficConfig(
        senders_per_wave=64,
        number_of_waves=120,
        first_wave_start_us=0,
        wave_interval_us=3_000,
        max_start_offset_us=30,
        seed=23,
        bytes_per_sender_per_wave=256 * 1024,
        packet_size_bytes=1_500,
        control_packet_every_n=20,
    )


SCENARIOS = {
    ScenarioName.NORMAL_TRAFFIC: normal_traffic,
    ScenarioName.HIGH_CONGESTION: high_congestion,
    ScenarioName.CONGESTION_AVOIDANCE: congestion_avoidance,
}


def get_scenario(name: ScenarioName) -> TrafficConfig:
    return SCENARIOS[name]()

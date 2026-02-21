from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class WaveStart:
    wave_id: int
    sender_id: int
    sender_start_us: int


def generate_wave_starts(
    *,
    senders_per_wave: int,
    number_of_waves: int,
    first_wave_start_us: int,
    wave_interval_us: int,
    max_start_offset_us: int = 0,
    seed: int = 0,
) -> list[WaveStart]:
    if senders_per_wave <= 0:
        raise ValueError("senders_per_wave must be > 0")
    if number_of_waves <= 0:
        raise ValueError("number_of_waves must be > 0")
    if first_wave_start_us < 0:
        raise ValueError("first_wave_start_us must be >= 0")
    if wave_interval_us < 0:
        raise ValueError("wave_interval_us must be >= 0")
    if max_start_offset_us < 0:
        raise ValueError("max_start_offset_us must be >= 0")

    jitter_rng = random.Random(seed)
    schedule: list[WaveStart] = []

    for wave_id in range(number_of_waves):
        wave_start_us = first_wave_start_us + wave_id * wave_interval_us
        for sender_id in range(senders_per_wave):
            start_offset_us = jitter_rng.randint(0, max_start_offset_us)
            sender_start_us = wave_start_us + start_offset_us
            schedule.append(
                WaveStart(
                    wave_id=wave_id,
                    sender_id=sender_id,
                    sender_start_us=sender_start_us,
                )
            )

    schedule.sort(key=lambda x: (x.sender_start_us, x.wave_id, x.sender_id))
    return schedule

"""Runtime sanity checks for generated traffic events."""

from __future__ import annotations

from collections import defaultdict

from .config import TrafficConfig
from .models.classifier import TrafficClass
from .schema import TrafficEvents


def validate_non_empty(events: TrafficEvents) -> None:
    """Ensure generation produced at least one traffic event."""
    if not events:
        raise ValueError("Generated traffic is empty.")


def validate_timestamp_order(events: TrafficEvents) -> None:
    """Ensure events are sorted by non-decreasing packet start time."""
    previous_ts = events[0].packet_start_us
    for event in events[1:]:
        if event.packet_start_us < previous_ts:
            raise ValueError("Traffic events are not sorted by packet_start_us.")
        previous_ts = event.packet_start_us


def validate_wave_sender_coverage(events: TrafficEvents, config: TrafficConfig) -> None:
    """Ensure each wave includes all expected sender IDs exactly once or more."""
    senders_by_wave: dict[int, set[int]] = defaultdict(set)
    for event in events:
        senders_by_wave[event.wave_id].add(event.sender_id)

    expected_senders = set(range(config.senders_per_wave))
    expected_waves = set(range(config.number_of_waves))

    actual_waves = set(senders_by_wave)
    if actual_waves != expected_waves:
        missing_waves = sorted(expected_waves - actual_waves)
        extra_waves = sorted(actual_waves - expected_waves)
        raise ValueError(
            f"Wave mismatch. missing_waves={missing_waves}, extra_waves={extra_waves}"
        )

    for wave_id in sorted(expected_waves):
        actual_senders = senders_by_wave[wave_id]
        if actual_senders != expected_senders:
            missing_senders = sorted(expected_senders - actual_senders)
            extra_senders = sorted(actual_senders - expected_senders)
            raise ValueError(
                f"Sender coverage mismatch for wave {wave_id}. "
                f"missing_senders={missing_senders}, extra_senders={extra_senders}"
            )


def validate_control_ratio(
    events: TrafficEvents, config: TrafficConfig, tolerance: float = 0.01
) -> None:
    """
    Out of all generated packets, some are marked CONTROL (high priority) and the rest are BULK.
    This check verifies that the share of CONTROL packets is what you configured.
    """
    if tolerance < 0:
        raise ValueError("tolerance must be >= 0")

    control_count = sum(1 for event in events if event.traffic_class == TrafficClass.CONTROL)
    total_count = len(events)
    actual_ratio = control_count / total_count
    expected_ratio = 1.0 / config.control_packet_every_n

    if abs(actual_ratio - expected_ratio) > tolerance:
        raise ValueError(
            "Control ratio out of bounds. "
            f"expected={expected_ratio:.6f}, actual={actual_ratio:.6f}, tolerance={tolerance:.6f}"
        )


def validate_generated_traffic(events: TrafficEvents, config: TrafficConfig) -> None:
    """Run the default validation suite and raise on first failed check."""
    validate_non_empty(events)
    validate_timestamp_order(events)
    validate_wave_sender_coverage(events, config)
    validate_control_ratio(events, config)

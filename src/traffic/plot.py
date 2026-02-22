from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from traffic.config import ScenarioName, get_scenario
from traffic.generator import generate_traffic
from traffic.models.classifier import TrafficClass


def _scenario_from_string(value: str) -> ScenarioName:
    try:
        return ScenarioName(value)
    except ValueError as exc:
        allowed = ", ".join(item.value for item in ScenarioName)
        raise argparse.ArgumentTypeError(
            f"Invalid scenario '{value}'. Choose one of: {allowed}"
        ) from exc


def _plot_scatter_packet_starts(events, out_dir: Path) -> None:
    times = np.array([event.packet_start_us for event in events], dtype=np.int64)
    senders = np.array([event.sender_id for event in events], dtype=np.int64)
    classes = np.array(
        [1 if event.traffic_class == TrafficClass.CONTROL else 0 for event in events],
        dtype=np.int64,
    )

    plt.figure(figsize=(10, 4))
    plt.scatter(times[classes == 0], senders[classes == 0], s=2, alpha=0.4, label="BULK")
    plt.scatter(times[classes == 1], senders[classes == 1], s=3, alpha=0.8, label="CONTROL")
    plt.xlabel("packet_start_us")
    plt.ylabel("sender_id")
    plt.title("Packet Starts Over Time")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(out_dir / "packet_starts_scatter.png", dpi=150)
    plt.close()


def _plot_events_per_time_bin(events, out_dir: Path, bins: int = 100) -> None:
    times = np.array([event.packet_start_us for event in events], dtype=np.int64)
    plt.figure(figsize=(10, 4))
    plt.hist(times, bins=bins)
    plt.xlabel("packet_start_us")
    plt.ylabel("event_count")
    plt.title("Events Per Time Bin")
    plt.tight_layout()
    plt.savefig(out_dir / "events_histogram.png", dpi=150)
    plt.close()


def _plot_control_ratio(events, config, out_dir: Path) -> None:
    total = len(events)
    control_count = sum(1 for event in events if event.traffic_class == TrafficClass.CONTROL)
    control_ratio = control_count / total if total else 0.0
    target_ratio = 1.0 / config.control_packet_every_n

    plt.figure(figsize=(6, 4))
    plt.bar(["target", "observed"], [target_ratio, control_ratio], color=["#7a7a7a", "#2f7ed8"])
    plt.ylim(0, max(target_ratio, control_ratio) * 1.2 if total else 1)
    plt.ylabel("control_fraction")
    plt.title("Control Ratio Check")
    plt.tight_layout()
    plt.savefig(out_dir / "control_ratio_bar.png", dpi=150)
    plt.close()


def _plot_wave_sender_bytes(events, config, out_dir: Path) -> None:
    bytes_by_wave_sender = defaultdict(int)
    for event in events:
        bytes_by_wave_sender[(event.wave_id, event.sender_id)] += event.packet_size_bytes

    matrix = np.zeros((config.number_of_waves, config.senders_per_wave), dtype=np.int64)
    for wave_id in range(config.number_of_waves):
        for sender_id in range(config.senders_per_wave):
            matrix[wave_id, sender_id] = bytes_by_wave_sender[(wave_id, sender_id)]

    plt.figure(figsize=(10, 5))
    plt.imshow(matrix, aspect="auto", interpolation="nearest")
    plt.colorbar(label="total_bytes")
    plt.xlabel("sender_id")
    plt.ylabel("wave_id")
    plt.title("Per-Wave Bytes Heatmap")
    plt.tight_layout()
    plt.savefig(out_dir / "wave_sender_bytes_heatmap.png", dpi=150)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate sanity plots for traffic output.")
    parser.add_argument(
        "--scenario",
        type=_scenario_from_string,
        default=ScenarioName.NORMAL_TRAFFIC,
        help="Scenario name.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("src/traffic/data/plots"),
        help="Directory where plot images are written.",
    )
    args, _ = parser.parse_known_args()

    config = get_scenario(args.scenario)
    events = generate_traffic(config)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    _plot_scatter_packet_starts(events, args.out_dir)
    _plot_events_per_time_bin(events, args.out_dir)
    _plot_control_ratio(events, config, args.out_dir)
    _plot_wave_sender_bytes(events, config, args.out_dir)

    print(f"Wrote 4 plots to: {args.out_dir}")


if __name__ == "__main__":
    main()

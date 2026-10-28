"""Create a bar chart from summary.json."""
import argparse
import json
from pathlib import Path
import sys

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Missing dependency: install matplotlib with: python -m pip install matplotlib", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Plot average device temperatures.")
    parser.add_argument("--input", default="summary.json", help="Input summary JSON path")
    parser.add_argument("--output", default="average_temperature.png", help="Output PNG path")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"Error: JSON file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        with input_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Error reading JSON: {error}", file=sys.stderr)
        return 1

    if not isinstance(data, list):
        print("Error: expected a JSON list of device summaries.", file=sys.stderr)
        return 1
    if not data:
        print("No data available for chart; summary JSON is empty.")
        return 0

    try:
        device_ids = [str(item["device_id"]) for item in data]
        averages = [float(item["average_temperature"]) for item in data]
    except (KeyError, TypeError, ValueError) as error:
        print(f"Error: JSON has an unexpected structure: {error}", file=sys.stderr)
        return 1

    width = max(8, len(device_ids) * 1.1)
    fig, ax = plt.subplots(figsize=(width, 5.5), constrained_layout=True)
    bars = ax.bar(device_ids, averages)
    ax.set_title("Average Temperature per Device", pad=14)
    ax.set_xlabel("Device ID")
    ax.set_ylabel("Average Temperature")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)
    ax.bar_label(bars, fmt="%.1f", padding=3)
    ax.tick_params(axis="x", labelrotation=30)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")

    fig.savefig(args.output, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Chart saved to: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

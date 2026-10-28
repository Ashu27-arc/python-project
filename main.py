"""Device Log Summarizer CLI.

Reads device_telemetry.csv, summarizes telemetry by device, filters devices
whose average temperature is above 80.0, exports JSON, and prints a table.
"""
import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


def clean_sensor_readings(values: list[Any]) -> list[float]:
    """Convert valid non-negative readings to floats and cap them at 500.0."""
    cleaned: list[float] = []

    for value in values:
        if value is None:
            continue

        try:
            number = float(value)
        except (TypeError, ValueError):
            continue

        # NaN and infinities are not useful sensor readings.
        if number != number or number in (float("inf"), float("-inf")):
            continue
        if number < 0:
            continue

        cleaned.append(min(number, 500.0))

    return cleaned


def summarize_csv(csv_path: Path, max_average: float = 80.0) -> list[dict[str, Any]]:
    """Read CSV and aggregate records by device_id, excluding bad rows."""
    if not csv_path.is_file():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    devices: dict[str, dict[str, Any]] = {}

    with csv_path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"device_id", "status", "temperature"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError(
                "CSV must contain these columns: device_id, status, temperature"
            )

        for line_number, row in enumerate(reader, start=2):
            device_id = (row.get("device_id") or "").strip()
            status = (row.get("status") or "").strip().upper()
            raw_temperature = row.get("temperature")

            if not device_id or raw_temperature is None:
                print(f"Warning: skipping incomplete row {line_number}.", file=sys.stderr)
                continue

            try:
                temperature = float(raw_temperature)
            except (TypeError, ValueError):
                print(f"Warning: skipping invalid temperature on row {line_number}.", file=sys.stderr)
                continue

            if temperature != temperature or temperature in (float("inf"), float("-inf")):
                print(f"Warning: skipping non-finite temperature on row {line_number}.", file=sys.stderr)
                continue

            if device_id not in devices:
                devices[device_id] = {
                    "device_id": device_id,
                    "total_records": 0,
                    "temperature_sum": 0.0,
                    "error_count": 0,
                }

            devices[device_id]["total_records"] += 1
            devices[device_id]["temperature_sum"] += temperature
            if status == "ERROR":
                devices[device_id]["error_count"] += 1

    results: list[dict[str, Any]] = []
    for device_id in sorted(devices):
        item = devices[device_id]
        average = item["temperature_sum"] / item["total_records"]
        if average > max_average:
            continue

        results.append({
            "device_id": device_id,
            "total_records": item["total_records"],
            "average_temperature": round(average, 2),
            "error_count": item["error_count"],
        })

    return results


def print_summary_table(results: list[dict[str, Any]]) -> None:
    """Print a small dependency-free table in the terminal."""
    headers = ("DEVICE ID", "TOTAL RECORDS", "AVG TEMP", "ERROR COUNT")
    rows = [
        (
            str(item["device_id"]),
            str(item["total_records"]),
            f'{item["average_temperature"]:.2f}',
            str(item["error_count"]),
        )
        for item in results
    ]
    widths = [
        max(len(headers[index]), *(len(row[index]) for row in rows))
        if rows else len(headers[index])
        for index in range(len(headers))
    ]

    def line(left: str, middle: str, right: str, fill: str) -> str:
        return left + middle.join(fill * (width + 2) for width in widths) + right

    print(line("+", "+", "+", "-"))
    print("|" + "|".join(f" {header:<{widths[i]}} " for i, header in enumerate(headers)) + "|")
    print(line("+", "+", "+", "="))
    for row in rows:
        print("|" + "|".join(f" {value:<{widths[i]}} " for i, value in enumerate(row)) + "|")
    print(line("+", "+", "+", "-"))
    if not results:
        print("No devices remain after validation and temperature filtering.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize device telemetry CSV data.")
    parser.add_argument("--input", default="device_telemetry.csv", help="Input CSV path")
    parser.add_argument("--output", default="summary.json", help="Output JSON path")
    args = parser.parse_args()

    try:
        results = summarize_csv(Path(args.input))
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as handle:
            json.dump(results, handle, indent=2)
            handle.write("\n")
        print_summary_table(results)
        print(f"\nJSON saved to: {output_path}")
        return 0
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

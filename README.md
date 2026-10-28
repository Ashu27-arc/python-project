# Device Log Summarizer CLI

A small Python command-line project for the Software Engineering Technical Assessment.

## Requirements
- Python 3.9+
- `matplotlib` only for chart generation; CSV processing uses Python's standard library.

## Files
- `main.py`: sensor reading sanitizer, CSV aggregation, temperature filter, JSON export, terminal table.
- `test_main.py`: 3 tests for Section 1.
- `plot_chart.py`: reads the generated JSON and writes a bar chart.
- `device_telemetry.csv`: illustrative sample input supplied with this project.
- `PROMPT_LOG.md`: example log template. Replace the example bug with the actual issue you observe during your own AI-assisted first attempt if different.

## Run
Run commands from this folder.

```bash
python main.py --input device_telemetry.csv --output summary.json
python -m unittest -v
python -m pip install matplotlib
python plot_chart.py --input summary.json --output average_temperature.png
```

On Windows, use `py` instead of `python` if needed.

## Notes
The assessment PDF refers to `device_telemetry.csv` but the CSV was not embedded in the provided PDF. The included CSV is sample data for demonstration; replace it with the actual assessment CSV if one was provided separately.
# python-project

# exporter.py

import csv
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

CACHE_FILE = Path("data/weather_cache.json")
console = Console()


def export_cache_to_csv(csv_file="weather_cache_export.csv"):
    """Exports the entire cached JSON into a CSV file."""
    if not CACHE_FILE.exists():
        print("❌ No cache file found.")
        return

    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)

    # Write CSV
    with open(csv_file, "w", newline="", encoding="utf-8") as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(["City", "Timestamp", "Temperature", "Wind Speed", "Wind Direction", "Previous Temperature"])

        for city, data in cache.items():
            payload = data["payload"]
            writer.writerow([
                city,
                data["timestamp"],
                payload.get("temperature"),
                payload.get("windspeed"),
                payload.get("winddirection"),
                data.get("previous")
            ])

    print(f"📄 CSV Export Complete: {csv_file}")


def print_cache_as_table():
    """Display cached data in a beautiful Rich table."""
    if not CACHE_FILE.exists():
        console.print("[bold red]❌ No cache file found.[/]")
        return

    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)

    table = Table(title="Weather Cache Data")

    # Define columns
    table.add_column("City", style="bold cyan")
    table.add_column("Timestamp", style="white")
    table.add_column("Temp (°C)", justify="center", style="magenta")
    table.add_column("Wind Speed", justify="center", style="cyan")
    table.add_column("Wind Dir", justify="center", style="blue")
    table.add_column("Previous Temp", justify="center", style="green")

    # Add rows from cache
    for city, data in cache.items():
        payload = data["payload"]
        table.add_row(
            city,
            data["timestamp"],
            str(payload.get("temperature")),
            str(payload.get("windspeed")),
            str(payload.get("winddirection")),
            str(data.get("previous")),
        )

    console.print(table)
import json
from pathlib import Path

file_path = Path(__file__).parent / "data" / "tick-sightings.json"

with file_path.open(encoding="utf-8") as file:
    sightings = json.load(file)
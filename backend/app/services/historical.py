import csv
from datetime import date
from pathlib import Path
from typing import Dict, List

from backend.app.config import HISTORICAL_DATA_PATH


def load_historical_data() -> List[Dict[str, object]]:
    if not HISTORICAL_DATA_PATH.exists():
        return []

    rows: List[Dict[str, object]] = []
    with HISTORICAL_DATA_PATH.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            rows.append({
                "date": row["date"],
                "visitors": int(row["visitors"]),
                "is_weekend": bool(int(row["is_weekend"])),
                "is_feriado": bool(int(row["is_feriado"])),
            })
    return rows


def get_baseline_for_date(target_date: date) -> Dict[str, float]:
    historical = load_historical_data()
    if not historical:
        return {"visitors": 160.0, "weekday_factor": 1.0, "weather_factor": 1.0}

    same_day = [row for row in historical if row["date"] == target_date.isoformat()]
    if same_day:
        row = same_day[0]
        base = float(row["visitors"])
        weekend_factor = 1.15 if row["is_weekend"] else 1.0
        holiday_factor = 1.12 if row["is_feriado"] else 1.0
        return {"visitors": base, "weekday_factor": weekend_factor, "weather_factor": holiday_factor}

    # Estimación semanal basada en promedio de días similares.
    weekday = target_date.weekday()
    similar_days = [
        row for row in historical
        if date.fromisoformat(row["date"]).weekday() == weekday
    ]
    if not similar_days:
        return {"visitors": 160.0, "weekday_factor": 1.0, "weather_factor": 1.0}

    avg_visitors = sum(float(row["visitors"]) for row in similar_days) / len(similar_days)
    return {"visitors": avg_visitors, "weekday_factor": 1.0, "weather_factor": 1.0}

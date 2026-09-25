from datetime import date
from typing import Dict, List

from backend.app.config import LEVEL_THRESHOLDS
from backend.app.services.historical import get_baseline_for_date


def is_weekend(day: date) -> bool:
    return day.weekday() >= 5


def classify_level(visitors: float) -> str:
    if visitors >= LEVEL_THRESHOLDS["Alta"]:
        return "Alta"
    if visitors >= LEVEL_THRESHOLDS["Media"]:
        return "Media"
    return "Baja"


def predict_visitors_for_date(target_date: date, weather: Dict[str, float], weekend: bool) -> Dict[str, object]:
    baseline = get_baseline_for_date(target_date)
    base_visitors = float(baseline["visitors"])
    weekday_factor = float(baseline["weekday_factor"])
    weather_factor = float(baseline["weather_factor"])

    temperature = float(weather.get("temperature", 0.0))
    rain_probability = float(weather.get("rain_probability", 0.0))
    precipitation = float(weather.get("precipitation_mm", 0.0))

    temp_adjustment = 1 + max(0, (temperature - 25)) * 0.012
    rain_penalty = 1 - min(rain_probability / 100, 0.45)
    precip_penalty = 1 - min(precipitation / 12, 0.2)
    weekend_boost = 1.18 if weekend else 1.0

    estimated = base_visitors * weekday_factor * weather_factor * temp_adjustment * rain_penalty * precip_penalty * weekend_boost
    estimated = round(max(0, estimated), 2)
    return {
        "visitors": estimated,
        "level": classify_level(estimated),
        "weekend": weekend,
    }

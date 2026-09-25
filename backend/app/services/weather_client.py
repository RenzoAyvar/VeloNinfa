import json
from datetime import date
from typing import Any, Dict, Optional

import httpx

from backend.app.config import API_KEY, LOCATION, WEATHER_BASE_URL


async def fetch_weather_for_date(target_date: date) -> Dict[str, Any]:
    if not API_KEY:
        return build_fallback_weather(target_date)

    params = {
        "key": API_KEY,
        "q": f"{LOCATION.latitude},{LOCATION.longitude}",
        "dt": target_date.isoformat(),
        "aqi": "no",
        "alerts": "no",
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(f"{WEATHER_BASE_URL}/forecast.json", params=params)
        response.raise_for_status()
        payload = response.json()

    forecast_day = (payload.get("forecast") or {}).get("forecastday") or []
    if not forecast_day:
        raise ValueError("No meteorological data available for the requested date.")

    day = forecast_day[0]
    day_info = day.get("day") or {}
    rain_mm = day_info.get("totalprecip_mm")
    temperature_c = day_info.get("maxtemp_c")
    rain_probability = day_info.get("daily_chance_of_rain")

    if temperature_c is None:
        temp = payload.get("current", {}).get("temp_c")
    else:
        temp = temperature_c

    return {
        "temperature": float(temp) if temp is not None else 0.0,
        "rain_probability": int(rain_probability) if rain_probability is not None else 0,
        "precipitation_mm": float(rain_mm) if rain_mm is not None else 0.0,
    }


def build_fallback_weather(target_date: date) -> Dict[str, Any]:
    day = target_date.day
    month = target_date.month
    base = 24 + ((day * 3 + month * 2) % 18)
    rain_probability = (day * 7 + month * 3) % 51
    precipitation = round((rain_probability / 100) * 8, 1)
    return {
        "temperature": float(base),
        "rain_probability": int(rain_probability),
        "precipitation_mm": float(precipitation),
    }

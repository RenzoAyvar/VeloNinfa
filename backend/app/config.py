import os
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class LocationConfig:
    name: str = "El Velo de las Ninfas"
    latitude: float = -9.430436
    longitude: float = -75.965934
    locality: str = "Tambillo Chico"
    district: str = "Mariano Dámaso Beraún"
    department: str = "Huánuco"
    country: str = "Perú"


LOCATION = LocationConfig()

API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_BASE_URL = "https://api.weatherapi.com/v1"

LEVEL_THRESHOLDS = {
    "Baja": 45,
    "Media": 90,
    "Alta": 150,
}

HISTORICAL_DATA_PATH = BASE_DIR / "app" / "data" / "historical_visitors.csv"

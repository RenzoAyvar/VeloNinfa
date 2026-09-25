from datetime import date
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from backend.app.config import LOCATION
from backend.app.services.predictor import is_weekend, predict_visitors_for_date
from backend.app.services.weather_client import fetch_weather_for_date

app = FastAPI(title="VeloPredict API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).resolve().parent.parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
def serve_index() -> FileResponse:
    return FileResponse(static_dir / "index.html")


@app.get("/api/v1/prediction")
async def get_prediction(
    date_value: str = Query(..., alias="date", description="Date in YYYY-MM-DD format")
) -> Dict[str, Any]:
    try:
        target_date = date.fromisoformat(date_value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Debe seleccionar una fecha válida en formato YYYY-MM-DD.") from exc

    if target_date < date.today():
        raise HTTPException(status_code=400, detail="La fecha debe ser hoy o una fecha futura.")

    try:
        weather = await fetch_weather_for_date(target_date)
    except Exception as exc:  # pragma: no cover - runtime guard
        raise HTTPException(status_code=503, detail="No fue posible obtener los datos meteorológicos necesarios.") from exc

    weekend = is_weekend(target_date)
    prediction = predict_visitors_for_date(target_date, weather, weekend)

    return {
        "location": {
            "name": LOCATION.name,
            "latitude": LOCATION.latitude,
            "longitude": LOCATION.longitude,
        },
        "date": target_date.isoformat(),
        "weather": {
            "temperature": round(float(weather["temperature"]), 1),
            "rain_probability": int(weather["rain_probability"]),
            "precipitation_mm": round(float(weather["precipitation_mm"]), 1),
        },
        "prediction": {
            "visitors": int(round(float(prediction["visitors"]))),
            "level": prediction["level"],
        },
        "factors": {
            "weekend": bool(prediction["weekend"]),
        },
    }

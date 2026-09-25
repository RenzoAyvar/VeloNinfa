from datetime import date

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.predictor import classify_level, predict_visitors_for_date

client = TestClient(app)


def test_prediction_endpoint_valid_date():
    response = client.get("/api/v1/prediction?date=2026-10-12")
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["location"]["name"] == "El Velo de las Ninfas"
    assert payload["weather"]["temperature"] is not None
    assert payload["weather"]["rain_probability"] >= 0
    assert payload["prediction"]["visitors"] >= 0
    assert payload["prediction"]["level"] in {"Baja", "Media", "Alta"}


def test_prediction_endpoint_invalid_date():
    response = client.get("/api/v1/prediction?date=abc")
    assert response.status_code == 400
    assert "fecha válida" in response.json()["detail"]


def test_predictor_classification_bounds():
    assert classify_level(44) == "Baja"
    assert classify_level(45) == "Baja"
    assert classify_level(90) == "Media"
    assert classify_level(91) == "Media"
    assert classify_level(150) == "Alta"


def test_predictor_uses_weekend_flag():
    weather = {"temperature": 28, "rain_probability": 20, "precipitation_mm": 0.4}
    prediction = predict_visitors_for_date(date(2026, 10, 12), weather, weekend=True)
    assert prediction["weekend"] is True
    assert prediction["level"] in {"Baja", "Media", "Alta"}

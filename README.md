# VeloPredict

Proyecto de prototipo para estimar la afluencia turística de El Velo de las Ninfas usando condiciones meteorológicas y datos históricos.

## Stack

- Backend: FastAPI
- Frontend: HTML, CSS y JavaScript estático
- Predicción: algoritmo basado en clima, tipo de día y dataset histórico sintético

## Requisitos

- Python 3.11+
- Acceso a internet para WeatherAPI si se usa la API real

## Configuración

1. Crear un entorno virtual.
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Definir la clave de WeatherAPI:
   ```bash
   set WEATHER_API_KEY=tu_clave
   ```
   En Linux/macOS:
   ```bash
   export WEATHER_API_KEY=tu_clave
   ```
4. Ejecutar el servidor:
   ```bash
   uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Acceso

- Frontend: http://localhost:8000/
- API: http://localhost:8000/api/v1/prediction?date=2026-10-12

## Notas

- La ubicación está fija en el backend para El Velo de las Ninfas.
- Si no hay clave de WeatherAPI configurada, la app usa un modo de respaldo con datos simulados para permitir pruebas locales.

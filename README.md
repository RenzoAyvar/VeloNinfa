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

## Despliegue en AWS EC2

### 1) Preparar la instancia EC2

- Ubuntu 22.04 LTS
- Abrir puertos: 22 y 80
- Instalar dependencias del sistema:
  ```bash
  sudo apt-get update
  sudo apt-get install -y git python3 python3-venv python3-pip
  ```

### 2) Configurar el repositorio

Ejecución inicial en la instancia:

```bash
sudo mkdir -p /opt/velopredict
cd /opt/velopredict
sudo git clone https://github.com/<TU_USUARIO>/<TU_REPOSITORIO>.git .
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Preparar el servicio systemd

Copiar el archivo de ejemplo o crear el servicio:

```bash
sudo cp scripts/velopredict.service /etc/systemd/system/velopredict.service
sudo systemctl daemon-reload
sudo systemctl enable --now velopredict
```

### 4) Configurar variables de entorno

Asigna la clave de WeatherAPI en la instancia:

```bash
export WEATHER_API_KEY=tu_clave
```

O bien agrega la variable al archivo del servicio.

### 5) Verificar acceso

```bash
sudo systemctl status velopredict --no-pager
curl http://localhost:8000/
```

## GitHub Actions

El workflow definido en [.github/workflows/deploy.yml](.github/workflows/deploy.yml) ejecuta:

1. Instalación de dependencias.
2. Ejecución de pruebas con `pytest`.
3. Despliegue automático por SSH a EC2 sobre la rama `main`.

### Secrets requeridos en GitHub

- `EC2_HOST`
- `EC2_USER`
- `EC2_SSH_KEY`
- `WEATHER_API_KEY`

### Recomendación final

Para usar el despliegue real, reemplaza en [scripts/ec2-setup.sh](scripts/ec2-setup.sh) los marcadores:

```bash
https://github.com/<TU_USUARIO>/<TU_REPOSITORIO>.git
```

por tu URL real del repositorio GitHub.

#!/usr/bin/env bash
set -e

sudo apt-get update
sudo apt-get install -y git python3 python3-venv python3-pip

REPO_DIR="/opt/velopredict"
REPO_URL="https://github.com/<TU_USUARIO>/<TU_REPOSITORIO>.git"

sudo mkdir -p "$REPO_DIR"
if [ ! -d "$REPO_DIR/.git" ]; then
  sudo git clone "$REPO_URL" "$REPO_DIR"
fi

sudo chown -R "$USER:$USER" "$REPO_DIR"
cd "$REPO_DIR"
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

sudo tee /etc/systemd/system/velopredict.service > /dev/null <<EOF
[Unit]
Description=VeloPredict App
After=network.target

[Service]
User=$USER
WorkingDirectory=$REPO_DIR
Environment=WEATHER_API_KEY=
ExecStart=$REPO_DIR/.venv/bin/uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now velopredict
sudo systemctl status velopredict --no-pager

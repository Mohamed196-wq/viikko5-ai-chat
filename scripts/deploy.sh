#!/bin/bash
set -e

cd /home/ubuntu/viikko5

git pull --ff-only origin main

.venv/bin/python -m pip install -r requirements.txt

sudo -n systemctl restart viikko5.service

curl -fsS http://127.0.0.1:8002/ -o /dev/null

echo "Viikko 5 julkaistu onnistuneesti!"

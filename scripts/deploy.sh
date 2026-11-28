#!/bin/bash
set -e

cd /home/ubuntu/viikko5

git pull --ff-only origin main

.venv/bin/python -m pip install -r requirements.txt

printf "DEPLOY_SHA=%s\n" "$(git rev-parse HEAD)" > .deploy-version
sudo -n install -m 644 config/viikko5.service /etc/systemd/system/viikko5.service
sudo -n install -m 644 config/nginx-viikko5.conf /etc/nginx/snippets/viikko5.conf
sudo -n nginx -t
sudo -n systemctl reload nginx
sudo -n systemctl daemon-reload
sudo -n systemctl restart viikko5.service

curl --retry 10 --retry-connrefused --retry-delay 2 -fsS http://127.0.0.1:8002/ -o /dev/null

echo "Viikko 5 julkaistu onnistuneesti!"

SHA=$(git rev-parse HEAD)
curl --retry 10 --retry-connrefused --retry-delay 2 -fsS http://127.0.0.1:8002/health | .venv/bin/python -c 'import json,sys; assert json.load(sys.stdin)["sha"] == sys.argv[1]' "$SHA"
echo "Git SHA tarkistettu: $SHA"

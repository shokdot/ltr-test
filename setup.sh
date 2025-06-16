#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ABSOLUTE_RUN_SH="$SCRIPT_DIR/run.sh"

CRON_JOB="25 * * * * $ABSOLUTE_RUN_SH"

CRON_EXISTS=$(crontab -l 2>/dev/null | grep -F "$CRON_JOB")

sudo apt update
sudo apt install -y cron
sudo systemctl enable cron
sudo systemctl start cron

mkdir -p research
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

if [ -z "$CRON_EXISTS" ]; then
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Cron job added."
else
    echo "Cron job already exists."
fi

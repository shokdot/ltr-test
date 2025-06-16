#!/bin/bash

CRON_JOB="25 * * * * ./run.sh"
CRON_EXISTS=$(crontab -l 2>/dev/null | grep -F "$CRON_JOB")

sudo apt update
sudo apt install cron
sudo systemctl enable cron
sudo systemctl start cron
mkdir research
python3 -m venv venv
pip install -r requirments.txt
if [ -z "$CRON_EXISTS" ]; then
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Cron job added."
else
    echo "Cron job already exists."
fi
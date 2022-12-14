#!/usr/bin/env bash

echo "Executing the script!"
sleep 5

echo "Restart cron"
sudo service cron restart

echo "Create logs directory"
sudo mkdir -p /var/log/crawlclima/
sudo touch /var/log/crawlclima/cron.log
sudo chown -R epiuser:epiuser /var/log/crawlclima

echo "Starting celery worker"

exec celery --workdir crawlclima/ --config celeryconfig -A fetchapp worker -B --loglevel=INFO

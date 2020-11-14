#!/usr/bin/env bash

cd /home/bitnami/backend
sudo ./manage.py migrate --settings backend.settings.production
sudo ./manage.py set_su --settings backend.settings.production
sudo ./manage.py collectstatic --settings backend.settings.production --noinput
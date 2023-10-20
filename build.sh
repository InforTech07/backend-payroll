#!/usr/bin/env sh
# exit on error

set -o errexit

pip install -r ./requirements/requirments.txt
python manage.py collectstatic --no-input
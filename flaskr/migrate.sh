#!/usr/bin/env sh
python -m flask db init
python -m flask db migrate -m "Init"
cd .. && gunicorn -w 4 -b 0.0.0.0:8000 flaskr.main:app



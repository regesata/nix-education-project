#!/usr/bin/env sh
python -m flask db init
python -m flask db migrate -m "Init"
python -m flask run --host=0.0.0.0



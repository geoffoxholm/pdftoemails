#!/bin/bash
mkdir -p uploads
export FLASK_APP=service.py
python3 -m flask run --host=0.0.0.0 --port=50001

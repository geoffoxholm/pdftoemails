#!/bin/bash
mkdir uploads
export FLASK_APP=pdftoemail.py
python -m flask run --host=0.0.0.0 --port=50001

#!/bin/bash
mkdir upload
export FLASK_APP=pdftoemail.py
python -m flask run --host=0.0.0.0

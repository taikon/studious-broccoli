#!/bin/bash
export PYTHONPATH="${PYTHONPATH}:$PWD"
source .venv/bin/activate
python app.py

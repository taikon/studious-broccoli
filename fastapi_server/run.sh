#!/bin/bash
export PYTHONPATH="${PYTHONPATH}:$PWD"
source .venv/bin/activate
uvicorn main:app --reload --workers 4 --host 0.0.0.0 --port 8188

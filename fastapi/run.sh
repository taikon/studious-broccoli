#!/bin/bash
export PYTHONPATH="${PYTHONPATH}:$PWD"
source .venv/bin/activate
uvicorn main:app --reload --workers 4

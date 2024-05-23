# Medical Charting App - FastAPI Server

### Introduction
- This sets up the LLM portion of the medical-charting-app. 
- Note that Groq client is being used for development, but in production it will use OpenLLM instead. 
- This server uses FastAPI and will run on a separate home server.

### Quickstart
- Install dependencies
  ```python
  python3 -m venv .venv
  pip install -r requirements.txt
  ```

- Allow `run.sh` to be executable
  ```python
  chmod +x run.sh
  ```

- Run the server
  ```python
  ./run.sh
  ```


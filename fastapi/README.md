# Medical Charting App - FastAPI Server

### Introduction
- This sets up the LLM portion of the medical-charting-app. 
- Note that Huggingface Serverless Inference API is being used for development, but in production it will use OpenLLM instead. 
- This server uses FastAPI and will run on a separate home server.

### Development Quickstart
- Install dependencies
  ```python
  python3 -m venv .venv
  pip install -r dev_requirements.txt
  ```

- Allow `run.sh` to be executable
  ```python
  chmod +x run.sh
  ```

- Run the server
  ```python
  ./run.sh
  ```


### Production Quickstart
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


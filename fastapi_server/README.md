# Medical Charting App - FastAPI Server

### Introduction
- This sets up the LLM portion of the medical-charting-app. 
- Note that Huggingface Serverless Inference API is being used for development, but in production it will use OpenLLM instead. 
- This server uses FastAPI and will run on a separate home server.
- To make API requests to the FastAPI server, you must include an Authorization Bearer token formatted as `f"Bearer {ACCESS_TOKEN}"`. The `ACCESS_TOKEN` is retrieved from the environment variable. Combining this with IP whitelisting will adequately secure the server.
- Using Ollama API because it's significantly faster vs `transformers` pipeline.

### Development Quickstart
- Install dependencies
  ```bash
  python3 -m venv .venv
  pip install -r dev_requirements.txt
  ```

- Allow `run.sh` to be executable
  ```bash
  chmod +x run.sh
  ```

- Run the server
  ```bash
  ./run.sh
  ```

### Production Quickstart
- Install [ollama](https://github.com/ollama/ollama)
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

- Run ollama in background on port 8188
  ```bash
  tmux new -s ollama
  ollama:~$ export OLLAMA_HOST="0.0.0.0:8188"
  ollama:~$ ollama serve
  ```

- For first time setup, also need to download llama3
  ```bash
  tmux new -s llama3
  llama3:~$ ollama run llama3
  llama3:~$ exit
  ```

- Add environment variables. `OLLAMA_API_ENDPOINT` should point to a custom host on port 8188.
  ```bash
  cp .env.example .env
  openssl rand -hex 32 >> .env # Then set this to the ACCESS_TOKEN
  ```

- Install dependencies
  ```bash
  python3 -m venv .venv
  pip install -r requirements.txt
  ```

- Allow `run.sh` to be executable
  ```bash
  chmod +x run.sh
  ```

- Run the FastAPI server
  ```bash
  ./run.sh
  ```

### Usage
- Go to `/redoc` and `/docs` in the browser to see the API reference and interactive API documentation, respectively.
- The interactive API docs require you click the `Authorize` button and input the `ACCESS_TOKEN` when making requests. Do not put the `Bearer` prefix in the input field when testing API endpoints within the interactive API docs directly.


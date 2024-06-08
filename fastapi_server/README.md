# Medical Charting App - FastAPI Server

### Introduction
- This sets up the LLM portion of the medical-charting-app. 
- This server uses FastAPI and will run on a home server. FastAPI will communicate with the Ollama API, which is also run on the home server.
- It makes use of the Ollama API because it's significantly faster vs `transformers` pipeline.
- To make API requests to the FastAPI server, you must include an Authorization Bearer token formatted as `f"Bearer {ACCESS_TOKEN}"`. The `ACCESS_TOKEN` is retrieved from the environment variable. Combining this with IP whitelisting will adequately secure the server.

### Quickstart
- Install [ollama](https://github.com/ollama/ollama)
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

- Run ollama in background on default port 11434
  ```bash
  tmux new -s ollama
  ollama:~$ chmod +x ollama.sh
  ollama:~$ ./ollama.sh
  ```

- For first time setup, also need to download llama3 7B
  ```bash
  tmux new -s llama3
  llama3:~$ ollama run llama3
  llama3:~$ exit
  ```

- Add environment variables. `OLLAMA_API_ENDPOINT` should point to the default port 11434.
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

- Run Cloudflare tunnel
  ```bash
  tmux new -s fastapi_cloudflare
  fastapi_cloudflare:~$ ./api_cloudflare.sh
  ```

### Usage
- Go to `http://localhost:8000/redoc` and `http://localhost:8000/docs` to see the API reference and interactive API documentation, respectively.
- The interactive API docs require you click the `Authorize` button and input the `ACCESS_TOKEN` when making requests. Do not put the `Bearer` prefix in the input field when testing API endpoints within the interactive API docs directly.


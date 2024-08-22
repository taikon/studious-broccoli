# Medical Charting App

### Introduction
- There are 2 directories in this project, `frontend` and `backend`.
- The backend requires the `ollama` CLI tool to serve llama3 7B.
- This application can be entirely self-hosted. Meaning that you can use it on your clinic's WiFi.

### Overview
- `frontend/`: React frontend.
- `backend/`: FastAPI backend. 
  - It communicates with ollama and the React frontend. 
  - It uses the `openbmb/MiniCPM-Llama3-V-2_5` vision model for handwritten text recognition.
- `ollama`: A CLI tool to serve ML models.
  - This is used to summarize and format the medical chart text.

### Experiments
- Handwritten Text Recognition:
  - `githubharald/HTRPipeline`: Not good.
  - `llava:34b`: Doesn't work at all. I suspect more because ollama is not able to access the file at all.
  - `harshit543/Handwritten-Text-Recognition`: It's okay. It works but can misinterpret maybe ~10% of the text. It's not good enough for production. 
  - `MiniCPM-Llama3-V-2_5`: Really good. Better than `harshit543/Handwritten-Text-Recognition`. Works well on Gradio, but unable to read image when used with ollama.
    - This has been integrated into the FastAPI backend.

- Model Inference:
  - `transformers`: Slow. Takes ~10 seconds to process a single page of text.
  - `ollama`: Fast. Takes ~1 second to process a single page of text.

## Getting Started
### Getting Started - Ollama
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

- The first time you run ollama, you need to download llama3 7B. This is done in a temporary tmux session. After the download is complete, you can exit the session. You only need to do this once.
  ```bash
  tmux new -s llama3
  llama3:~$ ollama run llama3
  llama3:~$ exit
  ```

### Getting Started - FastAPI
- Setup FastAPI environment variables. The `.env.example` file has `OLLAMA_API_ENDPOINT` set to the default port 11434.
  ```bash
  cd backend
  cp .env.example .env
  perl -pi -e 'chomp if eof' .env # Remove the last newline in .env
  openssl rand -hex 32 >> .env # Set this to the ACCESS_TOKEN
  ```

- Install dependencies
  ```bash
  cd backend
  python3 -m venv .venv
  pip install -r requirements.txt
  ```

- Allow `run.sh` to be executable
  ```bash
  chmod +x run.sh
  ```

- Run the FastAPI backend
  ```bash
  tmux new -s fastapi
  fastapi:~$ cd backend
  fastapi:~$ ./run.sh
  ```

- Run Cloudflare tunnel for FastAPI backend
  ```bash
  tmux new -s fastapi_cloudflare
  fastapi_cloudflare:~$ ./backend_cloudflare.sh
  ```

### Getting Started - React
- Setup React environment variables manually.
  ```bash
  cd frontend
  cp .env.example .env
  vim .env
  ```
  - Set `VITE_FASTAPI_SERVER_API_BASE_URL` to `https://api.<domain-name>.com`.
  - Set `VITE_TIPTAP_JWT` to the "Authentication" value in Tiptap dashboard settings.
  - Set `VITE_TIPTAP_COLLAB_APP_ID` to the "App ID" in the Tiptap dashboard.
  - Set `VITE_FASTAPI_SERVER_ACCESS_TOKEN` to `ACCESS_TOKEN` from `backend/.env`.

- Install dependencies.
  ```bash
  cd frontend
  pnpm install
  ```

- Run React frontend on port 4173.
  ```bash
  tmux new -s react
  react:~$ cd frontend
  react:~$ pnpm run build
  react:~$ pnpm run preview --port 4173
  ```

- Run Cloudflare tunnel for React frontend
  ```bash
  tmux new -s react_cloudflare
  react_cloudflare:~$ ./frontend_cloudflare.sh
  ```

- Go to `dashboard.<domain-name>.com`. The backend is hosted at `api.<domain-name>.com`.
- Allow 30-60 seconds for the application to load the first time you use the application or after restarting. This delay happens because the LLM must be loaded into memory.
- You can also load the LLM into memory prior to using the application.
- To do this, go to `api.<domain-name>.com/docs#/default/healthcheck_healthcheck_get`. Click "Try it out"  then click "Execute". When you see "ok" in the "Response body", the LLM has been loaded into memory.

### Usage
1. Go to `dashboard.<domain-name>.com` on your phone and login.
2. Click "Choose Files". This opens the default camera on your phone.
3. Take photos of the patient intake forms.
4. On your work computer, go to `dashboard.<domain-name>.com` and login.
5. The application will write a chart note using the patient intake forms. You can copy this form into your own EMR.

### Restarting Application
- This section requires you to have already run through [Getting Started](getting-started) at least once.
- Start all application processes.
  ```bash
  ./run.sh
  ```
- Gracefully stop the application.
  ```bash
  tmux kill-server
  ```

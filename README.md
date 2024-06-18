# Medical Charting App (Upperbound)

### Introduction
- There are 2 applications in this project, both run on a home server.

### Overview
- `frontend/`: React frontend.
- `backend/`: FastAPI backend. 
  - It communicates with ollama and the React frontend. 
  - It uses the `openbmb/MiniCPM-Llama3-V-2_5` vision model for handwritten text recognition.
- `ollama`: A CLI tool to serve ML models.
  - It is used to summarize and format the medical chart text.

### Experiments
- Handwritten Text Recognition:
  - `githubharald/HTRPipeline`: Not good.
  - `llava:34b`: Doesn't work at all. I suspect more because ollama is not able to access the file at all.
  - `harshit543/Handwritten-Text-Recognition`: It's okay. It works but can misinterpret maybe ~10% of the text. It's not good enough for production. 
  - `MiniCPM-Llama3-V-2_5`: Really good. Better than `harshit543/Handwritten-Text-Recognition`. Works well on Gradio, but unable to read image when used with ollama.
    - This has been integrated into `backend`

- Model Inference:
  - `transformers`: Slow. Takes ~10 seconds to process a single page of text.
  - `ollama`: Fast. Takes ~1 second to process a single page of text.

## Quickstart
### Quickstart - Ollama
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

### Quickstart - FastAPI
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
  fastapi_cloudflare:~$ ./api_cloudflare.sh
  ```

### Quickstart - React
- Setup React environment variables manually.
  ```bash
  cd frontend
  cp .env.example .env
  vim .env
  ```
  - Set `VITE_FASTAPI_SERVER_ACCESS_TOKEN` to `ACCESS_TOKEN` from `backend/.env`.
  - Set `VITE_FASTAPI_SERVER_API_BASE_URL` to `https://api.<domain-name>.com`.

- Install dependencies.
  ```bash
  cd frontend
  pnpm install
  ```

  - If you try to run `pnpm run dev` for development, you'll likely get a @/lib/utils path error. If this happens, you need to initialize `shadcn-ui`.
    ```bash
    pnpm dlx shadcn-ui@latest init 

    Would you like to use TypeScript (recommended)? yes
    Which style would you like to use? › Default
    Which color would you like to use as base color? › Slate
    Where is your global CSS file? › › src/index.css
    Do you want to use CSS variables for colors? › yes
    Where is your tailwind.config.js located? › tailwind.config.js
    Configure the import alias for components: › @/components
    Configure the import alias for utils: › @/lib/utils
    Are you using React Server Components? › no
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
  react_cloudflare:~$ ./dashboard_cloudflare.sh
  ```

- Go to `dashboard.<domain-name>.com`

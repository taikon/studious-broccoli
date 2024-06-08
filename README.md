# Medical Charting App (Upperbound)

### Introduction
- There are 2 applications in this project, both run on a home server.

### Overview
- `medicalcharting/`: React frontend.
- `fastapi_server/`: Handles communications between `MiniCPM-Llama3-V-2_5`, ollama and the React frontend.
- Ollama: A CLI tool. Handles LLM inference.

### Experiments
- Handwritten Text Recognition:
  - `githubharald/HTRPipeline`: Not good
  - `llava:34b`: Doesn't work at all. I suspect more because ollama is not able to access the file at all.
  - `MiniCPM-Llama3-V-2_5`: Really good. Better than `harshit543/Handwritten-Text-Recognition`. Works well on Gradio, but unable to read image when used with ollama.
    - This has been integrated into `fastapi_server`

### Quickstart
- Run ollama in background on default port 11434
  ```bash
  tmux new -s ollama
  ollama:~$ chmod +x ollama.sh
  ollama:~$ ./ollama.sh
  ```

- Run the FastAPI server
  ```bash
  ./run.sh
  ```

- Run Cloudflare tunnel for FastAPI server
  ```bash
  tmux new -s fastapi_cloudflare
  fastapi_cloudflare:~$ ./api_cloudflare.sh
  ```

- Run React frontend on port 8188.
  ```bash
  pnpm run build
  pnpm run preview --port 4173
  ```

- Run Cloudflare tunnel for React frontend
  ```bash
  tmux new -s react_cloudflare
  react_cloudflare:~$ ./dashboard_cloudflare.sh
  ```

- Go to `dashboard.<domain-name>.com`

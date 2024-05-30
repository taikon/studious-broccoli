# Medical Charting App - Gradio API

### Introduction
- This sets up the Handwriting Text Recognition portion of the medical-charting-app.
- This starts a Gradio application with API endpoints that are used by the FastAPI server. Similar to the FastAPI server, this is also run on the home server.
- It uses Gradio primary in the interest of development speed. But this can potentially be mounted onto the FastAPI server. Alternatively, you could move the code into the FastAPI server.
- It uses [MiniCPM-Llama3-V-2_5](https://huggingface.co/openbmb/MiniCPM-Llama3-V-2_5) 

### Quickstart
- Install dependencies
  ```bash
  python3 -m venv .venv
  pip install -r requirements.txt
  ```

- Allow `run.sh` to be executable
  ```bash
  chmod +x run.sh
  ```

- Run the Gradio server
  ```bash
  tmux new -s gradio
  gradio:~$ ./run.sh
  ```

### Usage
- This isn't used directly. Instead the FastAPI server interacts with the Gradio app's API endpoints.
- To find the API documentation, go to `http://localhost:7860` on your local machine and click on the "Use via API" at the bottom of the page.


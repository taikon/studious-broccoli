# Medical Charting App (Upperbound)

### Introduction
- There are 2 applications in this project.
- Application #1 is run locally on laptop.
- Application #2 is run on a home server.

### Overview
- `medicalcharting/`: React frontend.
- `MiniCPM-Llama3-V-2_5/`: Gradio app that performs Handwritten Text Recognition. It accepts an image and extracts text from it.
- `fastapi_server/`: Handles communications between `MiniCPM-Llama3-V-2_5`, ollama and the React frontend.
- Ollama: A CLI tool. Handles LLM inference.

### Experiments
- Handwritten Text Recognition:
  - `githubharald/HTRPipeline`: Not good
  - `llava:34b`: Doesn't work at all. I suspect more because ollama is not able to access the file at all.
  - `MiniCPM-Llama3-V-2_5`: Really good. Better than `harshit543/Handwritten-Text-Recognition`. Works well on Gradio, but unable to read image when used with ollama.

### Quickstart
- Look inside each directory for instructions.


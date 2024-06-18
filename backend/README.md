# Medical Charting App - FastAPI Server

### Introduction
- This sets up the LLM portion of the medical-charting-app. 
- This server uses FastAPI and will run on a home server. FastAPI will communicate with the Ollama API, which is also run on the home server.
- It makes use of the Ollama API because it's significantly faster vs `transformers` pipeline.
- To make API requests to the FastAPI server, you must include an Authorization Bearer token formatted as `f"Bearer {ACCESS_TOKEN}"`. The `ACCESS_TOKEN` is retrieved from the environment variable. Combining this with IP whitelisting will adequately secure the server.

### Quickstart
- See the "Quickstart - FastAPI" section in `./README.md` in the root directory.

### Usage
- Go to `http://localhost:8000/redoc` and `http://localhost:8000/docs` to see the API reference and interactive API documentation, respectively.
- The interactive API docs require you click the `Authorize` button and input the `ACCESS_TOKEN` when making requests. Do not put the `Bearer` prefix in the input field when testing API endpoints within the interactive API docs directly.


# Medical Charting App - FastAPI Backend

### Introduction
- FastAPI backend for the medical-charting-app.
- FastAPI communicates with the Ollama API.
- We use the Ollama API because it's significantly faster vs the `transformers` pipeline.
- To make API requests to the FastAPI server, you must include an Authorization Bearer token formatted as `f"Bearer {ACCESS_TOKEN}"`. The `ACCESS_TOKEN` is retrieved from the environment variable. Combining this with IP whitelisting will adequately secure the server.

### Getting Started
- See the "Getting Started - FastAPI" section in `./README.md` in the root directory.

### Usage
- Go to `http://localhost:8000/redoc` and `http://localhost:8000/docs` to see the API reference and interactive API documentation, respectively.
- The interactive API docs require you click the `Authorize` button and input the `ACCESS_TOKEN` when making requests. Do not put the `Bearer` prefix in the input field when testing API endpoints within the interactive API docs directly.

# Medical Charting App (Upperbound)

### Introduction
- There are 2 applications in this project.
- Application #1 is run locally on laptop.
- Application #2 is run on a home server.

### Overview
- Application #1 performs OCR on medical documents and extract text.
- Application #1 makes an API call to Application #2 with the extracted text.
- Application #2 processes the text with LLM and returns a JSON response.
- Application #1 receives the JSON response and displays it to the user.
  - Unsure: If no database is used, do we need to broadcast the JSON response using pubsub?

### Quickstart


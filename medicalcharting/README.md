# Medical Charting App - React Frontend

### Introduction
- This is the frontend portion of the medical-charting-app.

### Quickstart - Development
- Add environment variables. `VITE_FASTAPI_SERVER_ACCESS_TOKEN` should be the same as `ACCESS_TOKEN` in the FastAPI server.
- Install dependencies and run the development server on port 8188.
  ```bash
  pnpm install
  pnpm dlx shadcn-ui@latest init # If you get a @/lib/utils path error with pnpm run dev, it's because this wasn't run
  pnpm run dev --host 10.0.0.207 --port 8188
  ```

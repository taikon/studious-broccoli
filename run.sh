#!/bin/bash
echo "Starting application ..."

tmux new -d -s ollama "./backend/ollama.sh"
echo "Started ollama"

tmux new -d -s fastapi "cd ./backend && ./run.sh"
echo "Started fastapi"

tmux new -d -s fastapi_cloudflare "./backend/backend_cloudflare.sh"
echo "Started fastapi cloudflare"

tmux new -d -s react "pnpm --dir ./frontend/ run preview --port 4173"
echo "Started react"

tmux new -d -s react_cloudflare "./frontend/frontend_cloudflare.sh"
echo "Started react cloudflare"

echo "Application started"

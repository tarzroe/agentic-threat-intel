#!/bin/bash
set -e

# Configure for Hugging Face — use SQLite, skip Redis/Celery
export DATABASE_URL=sqlite:///./threatintel.db
export REDIS_URL=""
export HF_MODE=true

# Start backend in background
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --log-level warning &

# Wait for backend to be ready
sleep 3

# Start Streamlit frontend (foreground)
streamlit run frontend/app.py \
  --server.port 7860 \
  --server.address 0.0.0.0 \
  --server.headless true \
  --browser.serverAddress localhost \
  --browser.gatherUsageStats false

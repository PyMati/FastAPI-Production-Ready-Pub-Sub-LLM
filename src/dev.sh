#!/bin/sh

# Running FastAPI
fastapi dev main.py --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!

# Running Celery Worker
celery -A config worker --loglevel=info &
CELERY_PID=$!

# Wait for both processes to finish
wait $FASTAPI_PID
wait $CELERY_PID
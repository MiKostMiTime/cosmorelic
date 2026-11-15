# CosmoRelic — container deployment (Replit and any Docker host).
# Replit auto-detects this root Dockerfile and injects $PORT (typically 8080);
# app.py binds 0.0.0.0 on that port and falls back to 7860 locally.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

COPY requirements-runtime.txt .
RUN pip install --no-cache-dir -r requirements-runtime.txt

COPY . .

CMD ["python", "app.py"]

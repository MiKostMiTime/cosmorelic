# CosmoRelic — container deployment (Streamlit Community Cloud is the primary
# free host; this Dockerfile keeps any Docker host working as a fallback).
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860

WORKDIR /app

COPY requirements-runtime.txt .
RUN pip install --no-cache-dir -r requirements-runtime.txt

COPY . .

# Bind the port the host injects (Docker hosts set $PORT; fall back to 7860).
CMD ["sh", "-c", "streamlit run app.py --server.port ${PORT:-7860} --server.address 0.0.0.0"]
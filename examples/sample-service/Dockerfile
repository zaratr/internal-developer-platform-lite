FROM python:3.11-slim

# Create non-root user
RUN useradd -m nonroot
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml .
RUN pip install --no-cache-dir uv
RUN uv pip install --system .

COPY app app
COPY config config
COPY docker-compose.yml docker-compose.yml
COPY .env.example .env.example

USER nonroot
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

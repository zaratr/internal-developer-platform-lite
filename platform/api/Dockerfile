FROM python:3.11-slim

WORKDIR /app

COPY platform/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY platform/ ./platform/

EXPOSE 8000

CMD ["uvicorn", "platform.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

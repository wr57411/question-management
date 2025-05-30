FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    fastapi==0.68.1 \
    uvicorn==0.15.0 \
    python-multipart==0.0.5 \
    python-docx==0.8.11 \
    sqlalchemy==1.4.23

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 
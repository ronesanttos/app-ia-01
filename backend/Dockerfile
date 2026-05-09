FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Em dev, o compose sobrescreve com volume `.:/app`; as dependências ficam na imagem.
CMD ["celery", "-A", "project", "worker", "-l", "info"]

# Simple, reproducible container
FROM python:3.12-slim

# Avoid apt frontend prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install minimal runtime deps & create user
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 10001 app

WORKDIR /srv/app
COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./

# Security hardening basics
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GUNICORN_CMD_ARGS="--bind 0.0.0.0:8000 --workers 2 --threads 2 --timeout 30"

USER 10001
EXPOSE 8000

CMD ["gunicorn", "wsgi:application"]
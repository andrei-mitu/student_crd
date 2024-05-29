ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-alpine AS base

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apk add --no-cache \
    chromium-chromedriver \
    build-base \
    && rm -rf /var/cache/apk/*

WORKDIR /app
COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
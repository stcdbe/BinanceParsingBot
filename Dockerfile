FROM python:3.10-alpine

WORKDIR /bot

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY . .

RUN pip install --no-cache-dir --upgrade setuptools && \
    pip install --no-cache-dir --upgrade setuptools && \
    pip install --no-cache-dir -r requirements.txt

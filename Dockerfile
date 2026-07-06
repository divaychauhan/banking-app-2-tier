FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -v default-libmysqlclient-dev build-essentail pkg-config curl && \
    rm -rf /var/lib/apt/lists/*

COPY requireements.txt .
FROM python:3.10-slim

LABEL maintainer="Angel Moreno <chelito500@gmail.com>"

# Instalar compiladores y dependencias de sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["python", "app.py"]

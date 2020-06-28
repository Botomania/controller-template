FROM python:3.8-slim

RUN apt-get update -o Acquire::CompressionTypes::Order::=gz && \
    apt-get update && \
    apt-get install -y git

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python", "-u", "main.py"]

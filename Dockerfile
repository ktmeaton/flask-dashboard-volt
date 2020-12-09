FROM python:3.8

ENV FLASK_APP run.py

COPY run.py requirements.txt config.py .env ./
COPY app app

RUN pip install -r requirements.txt
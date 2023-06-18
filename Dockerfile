FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

WORKDIR /app

RUN apt-get update && \
    apt-get -y install libpq-dev gcc

RUN mkdir /app/static && \ 
    mkdir /app/media
    
RUN pip install poetry==1.4.2

COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry config virtualenvs.create false && \
    poetry install

COPY . .

EXPOSE 8000
###########
# BUILDER #
###########
FROM python:3.10-slim-bullseye as builder

WORKDIR /app
    
COPY ./pyproject.toml ./poetry.lock* /app/

RUN pip install --upgrade pip && \
    pip install poetry==1.4.2 && \
    poetry export --output requirements.txt --with dev --without-hashes && \
    pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


###############
# FINAL STAGE #
###############
FROM python:3.10-slim-bullseye as final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

WORKDIR /app

RUN apt-get update && \
    apt-get -y install libpq-dev gcc

RUN mkdir /app/staticfiles && \ 
    mkdir /app/mediafiles

COPY --from=builder /wheels /wheels

RUN pip install --upgrade pip && \
    pip install --no-cache /wheels/*

COPY . .

EXPOSE 8000
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /home/app/web

RUN apt-get update -y && apt-get upgrade -y

# i18n
RUN apt-get -y install gettext

COPY ./requirements.txt .
RUN pip install --default-timeout=500 --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /home/app/web/static

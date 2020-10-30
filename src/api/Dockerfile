FROM python:3
LABEL maintainer="manuso@usal.es"

ARG APP_NAME
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE $APP_NAME.extra_settings

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

RUN django-admin startproject $APP_NAME .
COPY extra_settings.py /code/$APP_NAME/

WORKDIR /
RUN git clone https://github.com/vishnubob/wait-for-it.git
WORKDIR /wait-for-it


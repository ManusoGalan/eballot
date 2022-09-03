# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt

# Copy needed files
COPY ballot_mgmt /code/ballot_mgmt
COPY api /code/api
COPY manage.py /code/

# Copy startup script on root
COPY init.sh /

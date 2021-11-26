FROM python:3.8-alpine

# set work directory
WORKDIR /flaskr

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP = main.py




RUN pip install pipenv
RUN apk add build-base

# install dependencies

COPY ./Pipfile .
COPY ./Pipfile.lock .
RUN  pipenv install --system --deploy

# copy project
COPY . .
EXPOSE 8000



FROM python:3.5.1

RUN apt-get update && \
    apt-get -y install postgresql-client libpq-dev --no-install-recommends

RUN mkdir /code
COPY . /code/
RUN cd /code/ && pip install -r requirements.txt
WORKDIR /code/

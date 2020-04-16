FROM python:3.7.7-alpine3.11

RUN mkdir -p /app

WORKDIR /app

COPY ./app/requirements.txt /app

RUN pip3 install -r ./requirements.txt

COPY ./app /app

EXPOSE 4082

ENTRYPOINT python3 ./server.py

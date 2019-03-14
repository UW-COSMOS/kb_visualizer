FROM python:alpine3.7

RUN apk update &&\
        apk add postgresql-dev gcc  musl-dev

WORKDIR /app/
COPY server.py /app/server.py
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8501
CMD python ./server.py $PG_CONN_STRING

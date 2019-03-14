FROM python:alpine3.7

RUN apk update &&\
        apk add postgresql-dev gcc  musl-dev postgresql

WORKDIR /app/
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY server.py /app/server.py
COPY setup.sh /app/
COPY schema.sql /app/
EXPOSE 8051
CMD python ./server.py $PG_CONN_STRING

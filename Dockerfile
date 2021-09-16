FROM alpine

FROM python

RUN mkdir /app

ADD echo_container.py /app

RUN  pip install flask

ENTRYPOINT python /app/echo_container.py

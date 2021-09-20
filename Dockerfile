FROM alpine

FROM python

RUN mkdir /image-repo

ADD app.py requirement.txt /image-repo

ADD app /image-repo/app

WORKDIR /image-repo

RUN  pip install -r requirement.txt

ENTRYPOINT python app.py

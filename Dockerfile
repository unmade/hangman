FROM python:3.8-alpine

COPY ./requirements/base.txt /requirements/
COPY ./requirements/prod.txt /requirements/

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make postgresql-dev \
    && apk add --no-cache postgresql-client \
    && pip install -r requirements/base.txt -r requirements/prod.txt \
    && apk del .build-deps gcc libc-dev make postgresql-dev

ENV HOME_DIR /usr/src/hangman
ENV PYTHONPATH=${HOME_DIR}

COPY ./start.sh ${HOME_DIR}/start.sh
RUN chmod +x ${HOME_DIR}/start.sh

COPY ./gunicorn_conf.py ${HOME_DIR}/gunicorn_conf.py

COPY ./alembic ${HOME_DIR}/alembic
COPY ./alembic.ini ${HOME_DIR}
COPY ./app ${HOME_DIR}/app
WORKDIR ${HOME_DIR}


EXPOSE 80

CMD ["./start.sh"]

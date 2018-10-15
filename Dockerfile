FROM python:3.6-alpine3.8

COPY src /app

WORKDIR /app

RUN cd /app && \
    apk --update add --no-cache postgresql postgresql-dev && \
    apk --update add --no-cache --virtual build-dependencies \
        build-base python-dev libffi-dev musl-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apk del build-dependencies

ENTRYPOINT [ "python", "/app/app.py" ]
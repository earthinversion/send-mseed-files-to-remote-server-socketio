FROM python:3.8.10

ENV PYTHONUNBUFFERED=TRUE

RUN pip install --no-cache-dir \
    gunicorn \ 
    python-socketio \
    cryptography \
    eventlet==0.30.2 \
    obspy

WORKDIR /code

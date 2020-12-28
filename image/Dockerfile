FROM python:alpine

RUN pip install pyyaml paho-mqtt psutil

COPY ./script/mqtt-status.py /src/mqtt-status.py
WORKDIR /src

CMD ["python","mqtt-status.py"]

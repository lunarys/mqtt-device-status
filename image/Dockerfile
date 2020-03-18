FROM python:alpine

RUN pip install pyyaml paho-mqtt

COPY ./script/mqtt-status.py /src/mqtt-status.py
WORKDIR /src

CMD ["python","mqtt-status.py"]

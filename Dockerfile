FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get -y install \
    build-essential \
    pkg-config \
    python3-pip \
    python3-tk \
    python3 \
    python3-dev

RUN pip3 install --upgrade pip

COPY requirements.txt .
RUN pip3 install --no-cache-dir --use-feature=2020-resolver -r requirements.txt

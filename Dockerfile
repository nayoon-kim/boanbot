FROM ubuntu:latest

MAINTAINER nayoonkym@gmail.com

WORKDIR /srv/boanbot

RUN apt-get update

# PIP
RUN apt-get update
RUN apt-get install -y python3.8 python3-pip --fix-missing
WORKDIR /srv/boanbot
COPY requirements.txt /srv/boanbot
RUN pip3 install -r requirements.txt

COPY . /srv/boanbot


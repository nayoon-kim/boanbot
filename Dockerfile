FROM ubuntu:latest

MAINTAINER nayoonkym@gmail.com

WORKDIR /srv/boanbot

RUN apt-get update

# PIP
RUN apt-get update
RUN apt-get install -y python3.8 python3-pip --fix-missing

# wget
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND=noninteractive

# CHROME
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/goodle.list'
RUN apt-get update
RUN apt-get install -y google-chrome-stable

# CHROME_DRIVER
RUN apt-get install -yqq unzip
RUN apt-get install -y curl
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
ENV DISPLAY=:99

WORKDIR /srv/boanbot
COPY requirements.txt /srv/boanbot
RUN pip3 install -r requirements.txt

COPY . /srv/boanbot

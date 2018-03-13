FROM ubuntu:16.04
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
	software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y \
	vim git-core python3.6 python3.6-dev \
	python3-pip build-essential libssl-dev libffi-dev python-dev

RUN mkdir /IDaaS
WORKDIR /IDaaS
ADD requirements.txt /IDaaS/
RUN python3.6 -m pip install -r requirements.txt
ADD . /IDaaS/

WORKDIR /IDaaS/IDaaS
VOLUME ["/IDaaS/IDaaS/IDaaS/conf"]

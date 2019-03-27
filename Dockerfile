FROM python:3.6.4

WORKDIR /Sakaar

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update -q
RUN apt-get install -yq netcat

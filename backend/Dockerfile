FROM python:3.7

RUN apt-get update
RUN apt-get install netcat -y

WORKDIR /backend

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . .

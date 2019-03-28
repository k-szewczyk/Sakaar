FROM python:3.6.7


WORKDIR /backend

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install netcat -y


COPY . .

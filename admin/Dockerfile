FROM python:3.8
ENV PYTHONNUMBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app
 

FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code/images/
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -U pip
RUN pip install -r requirements.txt
COPY . /code/


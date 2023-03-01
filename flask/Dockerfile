FROM python:3.8-slim

RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y default-libmysqlclient-dev

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--reload", "app:app"]

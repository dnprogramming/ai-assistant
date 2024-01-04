FROM --platform=linux/amd64 python:3.12

WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install google-chrome-stable -y

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]

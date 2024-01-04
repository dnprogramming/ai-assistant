FROM --platform=linux/amd64 python:3.12

WORKDIR /app

COPY . .

RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]

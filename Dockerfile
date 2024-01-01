FROM --platform=linux/amd64 python:3.12

WORKDIR /app

RUN apt-get update
RUN apt-get install apt-transport-https curl -y
RUN curl -fSsL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor | tee /usr/share/keyrings/google-chrome.gpg >> /dev/null
RUN echo deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main | tee /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update
RUN apt-get install google-chrome-stable -y

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]

# Use a base image with Python 3.12 runtime environment
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# Copy the application files to the container
COPY . .

# Install any dependencies required by your application
RUN pip install -r requirements.txt

# Specify the command to run your application
CMD [ "python", "main.py" ]

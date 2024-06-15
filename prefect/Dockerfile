# # Use the official Python image.
# # https://hub.docker.com/_/python
FROM --platform=amd64  python:3.8-slim

WORKDIR /app

COPY requirements.txt /app
COPY /packages /app/packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV DEVELOPMENT production

ADD . /app
EXPOSE 8080
CMD ["python", "/app/app.py"]



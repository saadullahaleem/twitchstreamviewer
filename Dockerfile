FROM python:3.6-slim
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y build-essential git libmagic-dev procps

# Allows docker to cache installed dependencies between builds
COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Adds our application code to the image
COPY ./ streameventviewer

EXPOSE 7000

# default command to execute
#CMD exec gunicorn streameventviewer.wsgi:application --bind 0.0.0.0:7000 --workers 3
CMD daphne -b 0.0.0.0 -p 7000 streameventviewer.asgi:application
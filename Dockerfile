FROM python:3.6-slim
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y build-essential git libmagic-dev procps

# Allows docker to cache installed dependencies between builds
COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Adds our application code to the image
COPY ./ streameventviewer

EXPOSE 7000

#CMD ./streameventviewer/scripts/wait-for-it.sh 10

## Run migrations
#CMD python ./streameventviewer/manage.py migrate
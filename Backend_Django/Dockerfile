
FROM python:3.7

RUN mkdir /app 
COPY . /app
WORKDIR /app

# #poetry add redis pylint-celery django-celery-beat celery
RUN pip3 install poetry
RUN poetry install    

# Running project
RUN chmod +x /app/initiator.sh
CMD ["/app/initiator.sh"]

ENV REDIS_HOST=127.0.0.1
ENV REDIS_PORT=6379

ENV PORT 8000
EXPOSE 8000

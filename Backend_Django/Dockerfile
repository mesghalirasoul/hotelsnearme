
FROM python:3.7

RUN mkdir /app 
COPY . /app
WORKDIR /app

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python && \
    mkdir -p /opt/dist

# ENV PATH "/root/.poetry/bin:${PATH}"
ENV PYTHONUNBUFFERED 1 
ENV PYTHONDONTWRITEBYTECODE 1

ENV XDG_CACHE_HOME=/root/.cache

RUN    pip3 install --upgrade \
        pip \
        pipenv \
        setuptools \
        wheel \
        gunicorn

RUN pip3 install poetry
RUN poetry install    

# Running project
RUN chmod +x /app/initiator.sh
CMD ["/app/initiator.sh"]

ENV REDIS_HOST=127.0.0.1
ENV REDIS_PORT=6379

ENV PORT 8000
EXPOSE 8000

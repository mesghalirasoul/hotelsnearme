# HotelsNearMe

## Welcome to HotelsNearMe
Welcome to hotelsnearme A full stack project including vuejs, django and postgres to find hotels near you using HEARAPI.

## Getting started
An at least basic understanding of the following technology is at least helpful if not mandatory! Please take the time to familiarize yourself by doing some tutorials. The days spent there will be worth as you will see later on (and you will bitterly regret if not)! Above all, you should be well familiar with the Python programming language and vuejs framework.

* [Django](https://docs.djangoproject.com/en/3.0/intro/tutorial01/)
* [DRF](https://www.django-rest-framework.org/) (and [CRUD REST API](https://sunscrapers.com/blog/ultimate-tutorial-django-rest-framework-part-1/))
* [Celery](https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)
* [Poetry](https://python-poetry.org/) (and the concept of virtual environments)
* [vuejs](https://v3.vuejs.org/guide/introduction.html)

Below is the structure of the project:

```bash
hotelsnearme/
├── Backend_Django
├── Frontend_vuejs
├── docker-compose.yml
├── heroku.yml
└── Postman Collection .json
```

### How to deploy the project on Heroku

The Backend project is already deployed on heroku you can check the APIs using postman collection and the following url:
```sh
https://hotelsnearme.herokuapp.com/
```
If you would like to deploy the backend project on heroku you need to create a new app in heroku and go to deploy tab ("App connected to GitHub") and link your git repository with heroku. Then heroku depolyment service will look for "heroku.yml" and deploy it easily. Do not forget to add these addons in the resource tab: 
```sh
heroku postgres  (backend database)
heroku redis (to cache requsest data)
```
### How to deploy the project on your local environment (using docker)
As the project is dockerized you can easily deploy the project using docker-compose command. you need to install docker and docker-compose on your machine.
```sh
docker-compose up
```
then try http://127.0.0.1 on the browser.

### How to deploy the project on your local environment (without docker)
if you prefer to deploy the project on your local host machine, instead of using docker, at first install postgresql and redis on your local machine then do the followings:

### Back-end project
install poetry python package management using the following command:

```sh
pip3 install poetry
pip install poetry
```
then go to the Backend_Django folder and run the below commands:

```sh
poetry install
poetry shell
./manage.py runserver
```
### Back-end Unit tests
Django test api used for test implementation. you can run those test using the following commands:

```sh
poetry shell
# All tests
./manage.py test
```
A postman collection already provided to you to test APIs in the Backend project!

### Front-end project
install node and vuejs the run the following command to run the project: the below linke shows how to install vuejs on your local machine: https://v3.vuejs.org/guide/installation.html#cli

### Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

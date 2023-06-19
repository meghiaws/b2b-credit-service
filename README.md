# B2B Credit Service

This is a simple B2B service for selling SIM card credits between different organizations.

## Features

- ✅ Authentication with email using JWT
- ✅ Increasing organizations balance when they requested such a thing
- ✅ Transfer credits between organizations
- ✅ Ability to view and update user profiles for organizations
- ✅ Production-ready configuration for Static Files, Database Settings, Gunicorn, Docker
- ✅ Clean architecture design
- ✅ Cloud-native design using 12-factor methodology

## Apps

There are 6 django apps in this project

- 🔋 `api`: Common thing related to api design (Pagination, Auth Mixins, ...)
- 🔋 `authentication`: Responsible for authentication and organization signup
- 🔋 `credits`: Main app, responsible for increasing credits, and transferring credits
- 🔋 `core`: Place to common stuff among project (BaseUser, ...)

## Technologies used

- ✨ [Python](https://www.python.org/) - Programming Language
- ✨ [Django](https://docs.djangoproject.com/en/4.2/) - Web Framework
- ✨ [Django REST Framework](https://www.django-rest-framework.org/) - For Building RESTful APIs
- ✨ [Docker](https://www.docker.com/) - Container Platform
- ✨ [PostgreSQL](https://www.postgresql.org/) - Database
- ✨ [Git](https://git-scm.com/doc) - Version Control System
- ✨ [Gunicorn](https://gunicorn.org/) - WSGI HTTP Server
- ✨ [Poetry](https://python-poetry.org/) - Package Manager

## Installation

Clone the project

``` git
git clone https://github.com/meghiaws/b2b-credit-service.git
```

⚠️ Note that there is a file called `.env.sample`, remove `.sample` postfix from that to make a `.env` file:

Now you can run the project

For running locally for test and develop:

```docker
docker compose up -d --build
```

And for running on the production:

```docker
docker compose -f docker-compose.prod.yml up -d --build
```

You currently have 2 containers running

- web
- db

You can access to app from `http://0.0.0.0:8000`

## API Documentations

You can also access to all of the endpoints with OpenAPI schemas

Using Swagger UI

```text
http://0.0.0.0:8000/api/docs
```

Using Redoc

```text
http://0.0.0.0:8000/api/redoc
```

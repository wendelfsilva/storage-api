# storage-api

This project was generated with [Python](https://www.python.org/downloads/release/python-380/) version 3.8.

Open the terminal in the project root folder and run all following commands

## Environment

Create and activate python environments and install dependencies to run the project.

```
$ python -m venv venv
```

- On Unix or MacOS, using the bash shell

```
$ source venv/bin/activate
```

- On Windows using PowerShell

```
$ venv\Scripts\Activate.ps1
```

## Install dependencies

Run `pip install -r requirements.txt` for install all dependencies in your python environment.

> **Note** : You must first activate python environments to install dependencies.

## Migrations

Run `python manage.py migrate` for execute all migrations and synchronize the database. I am using SQLite in this project.

## Development server

Run `python manage.py runserver 127.0.0.1:8000` for a dev server. Navigate to `http://127.0.0.1:8000/` to check django page. The app will automatically reload if you change any of the source files.

## Running unit tests

Run `python manage.py test` for run all tests. The app will automatically look for tests and try to run it.

## Further help

To get more help on the on Django check out the [Getting started with Django](https://www.djangoproject.com/start/) or [Django REST framework](https://www.django-rest-framework.org/) page.

## Users available

For default five users were created, bellow the credentials:

| Username | Password |
|----------|----------|
| user1    | 123456   |
| user2    | 123456   |
| user3    | 123456   |
| user4    | 123456   |
| user5    | 123456   |

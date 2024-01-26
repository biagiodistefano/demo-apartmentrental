# Demo Apartment rentals backend API

## About
This is a Django project that provides an API for apartment rentals.

It is powered by `Django` with `Django-Ninja` (instead of the bulky Django REST Framework).

The authentication is handled by `django-ninja-jwt`, and as the name suggests, it uses JWT tokens.

The database is `PostgreSQL`.

## Start with docker

In a hurry? Start the project with docker:

Note: make sure to set the correct permissions on your host machine for the media folder if you want to upload photos.

```bash
docker-compose --env-file=.env.docker up
```

## Main requirements
- Python 3.12
- Django 5.0.1

## Quickstart

### Installation
Make sure to have Python 3.12 installed and poetry installed with it.

*NOTE*: If you are running on a Mac (M1, M2, M3), see below.

run:

```bash 
poetry install --no-root
```

### Installation for Mac users
If you are running on a Mac (M1, M2, M3),
it's recommended to create first a virtual environment specifying the architecture of the Python interpreter:

```bash
arch -arm64 python3 -m venv .venv
```

Then, activate the virtual environment:

```bash
source .venv/bin/activate
```

Finally, install the dependencies:

```bash
poetry install  --no-root
```

### Bootstrapping the database

Note:
- make sure to start postgresql before running the following commands (`docker-compose --env-file=.env.defaults up postgres`)
- make sure to move into the `src` directory before running the following commands

There are two utilty scripts to bootstrap the database:

#### 1. `python manage.py bootstrap`

It will run the migrations and create a superuser.

The superuser username and password are loaded from the configuration file.

If not specified, the default username is `admin` and the default password is `admin`.
A warning will be displayed if the default credentials are used.

It will also create by default a Group named `realtor` that will be used for permissions.

#### 2. `python manage.py create-fake-data [--apartments <number>] [--users <number>] [--realtors <number>]`

It will create fake data for the apartments, users and realtors.
- Every user will have the following email: `user{x}@example.com`, where x is a number starting from 1.
- Every realtor will have the following email: `realtor{x}example.com`, where x is a number starting from 1.
- Every apartment will have a random realtor assigned to it. Will also have random fake data for the rest of the fields.

## Running the server

Note:
- make sure to start postgresql before running the following commands (`docker-compose --env-file=.env.defaults up postgres`)

To run the server locally, run the following command:

```bash
python manage.py runserver
```

This will load the settings from the `.env.defaults` file. If not found, it will attempt to load the settings from:
- the `.env` file.
- the `settings.ini` file.
- the environment variables.

To specify which settings file to use, set it as an environment variable:

```bash
USE_ENV=.env.production python manage.py runserver
```

The server will be available at `http://localhost:8000`.

The API Documentation will be available at `http://localhost:8000/api/docs`.

## Testing

This project has 100% test coverage.
To run the tests locally, run the following command:

```bash
pytest --cov=. src/tests/ -vv && coverage html
```

then open the `htmlcov/index.html` file in your browser.

## Linting and formatting

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting.

If desired, install the pre-commit hooks:

```bash
pre-commit install
```

If you want to run the linter manually, run:

```bash
ruff check . --fix
```

If you want to run the formatter manually, run:

```bash
ruff format .
```

## Considerations

This is a simple project, therefore due to its scale some shortcuts were taken:

- The buisness logic is in the views. For a bigger project, it would be better to move it to a service layer and create custom exception handlers.
- The object-permissions are hardcoded in the views. For a bigger project, it would be better to move them to a permission layer.
- Each apartment has a single realtor assigned to it. For a bigger project, it would be better to have a many-to-many relationship between apartments and realtors.
- The search functionality is very basic. For a bigger project, it would be better to use a search engine like Meilisearch or Elasticsearch.
- For the sake of simplicity, in the docker image this is deployed with a single gunincorn worker. For a bigger project, it would be better to use multiple workers with a combination of gunicorn and uvicorn, switching from WSGI to ASGI, making the necessary adjustments to the codebase (i.e., using the async ORM and enpoints).
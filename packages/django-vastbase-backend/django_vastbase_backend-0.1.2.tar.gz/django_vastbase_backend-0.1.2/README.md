# django-vastbase-backend

vastbase database dialect for django

## Requirements

- psycopg2-binary 2.9.10
- django >= 4.0

## Install

```shell
pip install django-vastbase-backend
```

## Usage

You can set the name in your Django project `settings.py` as:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django_vastbase_backend',
        'NAME': '<database name>',
        'USER': '<database username>',
        'PASSWORD': '<database password>',
        'HOST': '<database host>',
        'PORT': '5432',
    }
}
```
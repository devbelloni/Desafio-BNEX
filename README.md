# Product Catalog (Django): BNEX Challenge

![CI](https://github.com/devbelloni/Desafio-BNEX/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5-092E20)

A product catalog web application built for a hiring challenge: authenticated users can
list, search, view, create, edit and delete products.

## Features

- Full CRUD with Django class-based views, Bootstrap templates and form validation
- **Login required on every view** (Django admin authentication). Only the list page used to
  hide its content, while the create, edit and delete URLs were reachable by anonymous
  users; this version protects them all and has tests for it.
- Search by name and pagination (10 per page)
- **Money stored as `Decimal`** (two decimal places, non-negative validator) instead of
  floating point, which cannot represent cents exactly
- Django admin with search and list columns
- **Configuration from the environment**: no secret key in the repository, `DEBUG` off by
  default, configurable `ALLOWED_HOSTS`

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export DJANGO_DEBUG=1            # local development only (or set DJANGO_SECRET_KEY)
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver       # http://127.0.0.1:8000
```

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Secret key (required unless `DJANGO_DEBUG=1`) |
| `DJANGO_DEBUG` | `1` enables debug mode |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hosts (default `localhost,127.0.0.1`) |

## Tests

```bash
DJANGO_SECRET_KEY=test python manage.py test
```

Ten tests cover the model (ordering, validation, exact cents) and the views (login required
for all routes, anonymous POST cannot delete, search, pagination, the create, update and
delete flow, invalid input and 404). CI also checks that no migration is missing.

## Layout

```
bnex/       project settings and URLs
product/    models, views, admin, templates, tests, migrations
```

## Author

**Márcio Belloni**, AI/ML Engineer.
[LinkedIn](https://www.linkedin.com/in/marcio-belloni/) · [GitHub](https://github.com/devbelloni)

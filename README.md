# Investment tracker 📈

## Description

A simple investment tracker built with Django that models investment accounts and investment holdings. The REST API uses DRF (Django REST Framework).

## Directory Structure

<details>
     <summary> Click to expand </summary>
  
```
── core
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── investments
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models
│   │   ├── __init__.py
│   │   ├── abstract_holding.py
│   │   ├── account.py
│   │   ├── equity_holding.py
│   │   └── tests
│   ├── serializers
│   │   ├── __init__.py
│   │   ├── account.py
│   │   ├── equity_holding.py
│   │   └── tests
│   ├── tests.py
│   ├── urls.py
│   └── views
│       ├── __init__.py
│       ├── account.py
│       ├── equity_holding.py
│       ├── pagination.py
│       └── tests
├── manage.py
└── requirements.txt
```

</details>

## Endpoints

These endpoints provide functionality to manage accounts and investment holdings.

### Accounts

- Add account: `POST /account`
- Retrieve account details: `GET /account/<id>`

### Equity Holdings

- Add equity holding for an account: `POST /account/<account_id>/equity`
- List equity holdings for an account: `GET /account/<account_id>/equity`
- Retrieve equity holding details: `GET /account/<account_id>/equity/<id>`

## Install Dependencies

```base
pip install -r requirements.txt
```

## This project uses Postgres

I suggest using the psycopg2 adapter!

To get started make sure you have postgresql installed:

```bash
$ brew install postgresql
$ brew services start postgresql
$ pip install psycopg2
```

Once database is setup, run the migration commands:

```bash
$ python manage.py makemigrations
No changes detected
```

```bash
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
...
Applying sessions.0001_initial... OK
...
```

## Future improvements

- Support for other types of holdings (fixed income, crypto and more).
- Account model tracks remaining contribution space for registered accounts 🇨🇦 (TFSA and RRSP).

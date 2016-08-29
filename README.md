# flask-api-skeleton

[![Build Status](https://travis-ci.org/ianunruh/flask-api-skeleton.svg?branch=master)](https://travis-ci.org/ianunruh/flask-api-skeleton)
[![codecov](https://codecov.io/gh/ianunruh/flask-api-skeleton/branch/master/graph/badge.svg)](https://codecov.io/gh/ianunruh/flask-api-skeleton)

## Requirements

* Python 2.7+ or 3.5+

## Development

```bash
git clone https://github.com/ianunruh/flask-api-skeleton.git myapp
cd myapp

cp config.sample.yml config.yml

pip install -U -r requirements.txt

./manage.py db upgrade
./manage.py runserver -rd
```

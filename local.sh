#!/bin/bash

export FLASK_ENV=development
mkvirtualenv bec --python=python3
pip install -r requirements/base.txt
flask db init && flask db migrate && flask db upgrade
python manage.py seed_db
flask run

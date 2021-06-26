#!/bin/bash

docker compose down -v
docker compose up  --build -d --remove-orphans
docker-compose run web python manage.py seed_db
docker attach be-challenge-revenue
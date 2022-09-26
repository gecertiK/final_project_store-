#!/usr/bin/env sh

# Alembic migrations ...
flask db upgrade

# Admin creation
flask create_admin

# wsgi application
python wsgi.py
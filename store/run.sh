#!/usr/bin/env sh

# Alembic migrations ...
alembic upgrade head

uvicorn main:app --reload --host 0.0.0.0 --port 5002
#  FastAPI Configuration file

#!/usr/bin/env python

import os
from dotenv import load_dotenv

from pydantic import BaseSettings


load_dotenv()

# Find the absolute file path to the top level project directory
basedir = os.path.abspath(os.path.dirname(__file__))


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    class Config:
        env_file = "store.env"


settings = Settings()

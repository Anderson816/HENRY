config.py

import os

class Config: SECRET_KEY = os.getenv("SECRET_KEY", "you-will-never-guess") SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///instance/app.db") SQLALCHEMY_TRACK_MODIFICATIONS = False DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL") LANGUAGES = ['en', 'kn']


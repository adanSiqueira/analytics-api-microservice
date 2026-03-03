from decouple import config as decouple_config

DATABASE_URL = decouple_config("DATABASE_URL", default="")
if DATABASE_URL == "" or not DATABASE_URL:
    raise ValueError("DATABASE_URL needs to be set in environment variables.")

DB_TIMEZONE = decouple_config("DB_TIMEZONE", default="UTC")
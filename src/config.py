import os

from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

class Config:
    DB_URL = os.getenv("DB_URL")
    DB_API_KEY = os.getenv("DB_API_KEY")


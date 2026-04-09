import os

from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

class Config:

    @property
    @staticmethod
    def DB_URL() :
        return os.getenv("DB_URL")

    @property
    @staticmethod
    def DB_API_KEY() :
        return os.getenv("DB_API_KEY")


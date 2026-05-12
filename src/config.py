import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from supabase import ClientOptions, create_client

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)


class Config:
    DB_URL = os.getenv("DB_URL")
    DB_API_KEY = os.getenv("DB_API_KEY")

    DB = create_client(
        DB_URL,
        DB_API_KEY,
        ClientOptions(httpx_client=httpx.Client(trust_env=False)),
    )


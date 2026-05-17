import os
import httpx
import json

from pathlib import Path
from dotenv import load_dotenv
from supabase import ClientOptions, create_client

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

items = json.loads((Path(__file__).resolve().parent / "tags.json").read_text())
TAGS: dict[str, str] = {x["tag"]: x["color"] for x in items }

class Config:
    DB_URL = os.getenv("DB_URL")
    DB_API_KEY = os.getenv("DB_API_KEY")

    DB = create_client(
        DB_URL,
        DB_API_KEY,
        ClientOptions(httpx_client=httpx.Client(trust_env=False)),
    )


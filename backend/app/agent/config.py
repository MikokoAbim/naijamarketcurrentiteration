import os
from pathlib import Path

from dotenv import load_dotenv

# Project root = the folder containing NaijaMarketAgent (parent of backend/).
ROOT = Path(__file__).resolve().parent.parent.parent.parent

load_dotenv(ROOT / ".env")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

MODEL_NAME = os.getenv("MODEL", "deepseek/deepseek-v4-flash")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.6"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))

# Where skills will live on disk.
SKILLS_DIR = ROOT / os.getenv("SKILLS_DIR", "backend/app/agent/skills")


def require_api_key() -> str:
    if not OPENROUTER_API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing. Copy .env.example to .env and fill it in."
        )
    return OPENROUTER_API_KEY

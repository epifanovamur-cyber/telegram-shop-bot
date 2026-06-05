import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID_TEXT = os.getenv("ADMIN_ID")


if BOT_TOKEN is None:
    raise ValueError("BOT_TOKEN не найден. Проверь файл .env")

if ADMIN_ID_TEXT is None:
    raise ValueError("ADMIN_ID не найден. Проверь файл .env")


ADMIN_ID = int(ADMIN_ID_TEXT)
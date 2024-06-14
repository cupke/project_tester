# Third-party
from dotenv import load_dotenv

# Standard
import os
import pathlib


load_dotenv()

BASE = pathlib.Path(__file__).resolve().parent
LOGGING_PATH = BASE / 'logs'

gpt = {
    'key': os.getenv('OPENAI_API_KEY'),
    'base_url': 'https://api.proxyapi.ru/openai/v1',
}

bot = {
    'token': os.getenv('BOT_TOKEN')
}


if not os.path.exists(LOGGING_PATH):
    os.makedirs(LOGGING_PATH)

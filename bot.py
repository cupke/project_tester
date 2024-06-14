# Third-party
from aiogram import Bot, Dispatcher

# Project
import config as cf

bot = Bot(cf.bot['token'], parse_mode='Markdown')
dispatcher = Dispatcher(bot=bot)

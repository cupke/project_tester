# Third-party
from aiogram import Bot, Dispatcher

# Standard
import asyncio

# Project
import config as cf
from logger import logger
from handlers import commands_router
from bot import bot, dispatcher


async def start_bot():
    logger.clear_log_file()
    logger.info('Bot start')
    [dispatcher.include_router(router) for router in [commands_router]]
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(
        bot,
        allowed_updates=['message', 'callback_query']  # Add needed router updates
    )


if __name__ == '__main__':
    asyncio.run(start_bot())

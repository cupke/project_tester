# Third-party
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

# Project
from logger import logger
from bot import bot
from gpt import send_gpt_request, get_balance
import config as cf

commands_router = Router()


@commands_router.message(Command("start"))
async def handle_start_command(message: Message):
    logger.info(f"User {message.from_user.id} using command /start")
    await message.answer(
        text="Посмотрите на все доступные возможности и команды тут /help"
    )


@commands_router.message(Command("help"))
async def handle_help_command(message: Message):
    logger.info(f"User {message.from_user.id} using command /help")
    help_msg = """👋 Задайте интересующий вас вопрос и GPT ответит вам!

**/help** - Посмотреть все команды"""
    await message.answer(help_msg)


@commands_router.message(Command("balance"))
async def handle_balance_command(message: Message):
    logger.info(f"User {message.from_user.id} using command /balance")
    response = get_balance()
    balance = response.get('balance', 'Попробуйте еще раз!')
    if isinstance(balance, float):
        balance = f'Ваш баланс: {round(balance, 2)}₽'
    await message.answer(text=balance)


@commands_router.message(F.text)
async def handle_user_text_message(message: Message, prompt: str = None):
    logger.info(f"Redirecting user {message.from_user.id} message to gpt")
    sending_request_msg = await message.answer(
        "Отправляем Ваш запрос! Пожалуйста, подождите!"
    )
    user_msg = message.text if not prompt else prompt
    image_url = None
    if message.entities:
        for entity in message.entities:
            if entity.type in ["url"]:
                url = message.text[entity.offset:entity.offset + entity.length]
                if url.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_url = url
                    break
    if image_url:
        user_msg = user_msg.replace(image_url, '').strip()
    try:
        if image_url:
            gpt_response = await send_gpt_request(prompt=user_msg, image_url=image_url)
        else:
            gpt_response = await send_gpt_request(prompt=user_msg)
        
        await message.answer(text=gpt_response, parse_mode="Markdown")
    except Exception as e:
        logger.error(e)
        logger.error("GPT text generation error!")
        await message.answer("Возникли ошибки при отправке запроса! Попробуйте еще раз")
    await sending_request_msg.delete()


@commands_router.message(F.photo)
async def handle_image_recognition_input(message: Message, state: FSMContext):
    generating_msg = await message.answer(
        "Генерирование описания к изображению. Пожалуйста подождите!"
    )
    caption = message.caption if message.caption else ""
    try:
        if message.photo:
            image_file = await bot.get_file(
                message.photo[-1].file_id
            )
            image_url = f'https://api.telegram.org/file/bot{cf.bot["token"]}/{image_file.file_path}'
            response = await send_gpt_request(prompt=caption, image_url=image_url)
            await message.answer(text=response)
        else:
            await message.answer("Неправильный формат! Киньте изображение")
    except Exception as e:
        await message.answer("Произошла ошибка. Попробуйте еще раз!")
        logger.error(e)
        logger.error("GPT image recognition error!")
    await generating_msg.delete()
    await state.clear()

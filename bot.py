import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.bot import api
import aiohttp
import random
from time import sleep

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token='1359919586:AAG8rzjvD18zcMWJqLg-7Wd6beM1j88i8MY')
dp = Dispatcher(bot)


@dp.message_handler(commands=['help'])
async def send_menu(message: types.Message):
    """отправиь список команд бота"""
    await message.reply(
        text="""
        Это StyleTransferBot. Пришлите фотогрфаии\n
        Мои команды: 
        /start - приветсвенное сообщение
        /help -- увидеть помощь"""
    )


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """отправиь список команд бота"""
    await message.reply("Привет!\nЯ - StyleTransferBot!\nПришлите картинки, которые Вы хотите преобразовать")
    # await send_menu(message=message)


"""
@dp.message_handler(content_types=types.ContentType.TEXT)
async def do_echo(message: types.Message):
    text = message.text
    if text:
        await message.reply(text=text)
"""


@dp.message_handler(content_types=types.ContentType.TEXT)
async def style_transfer(message: types.Message):
    text = message.text
    # w = p.model(ll)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()

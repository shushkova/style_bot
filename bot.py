import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.bot import api
import asyncio
import aiohttp
import random
from time import sleep

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = 32100
TOKEN = '1359919586:AAG8rzjvD18zcMWJqLg-7Wd6beM1j88i8MY'
bot = Bot(token='1359919586:AAG8rzjvD18zcMWJqLg-7Wd6beM1j88i8MY')
dp = Dispatcher(bot)


WEBHOOK_HOST = 'https://immense-taiga-94950.herokuapp.com/' + TOKEN
WEBHOOK_PATH = ''
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 32102

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


class Form(StatesGroup):
    start_command = State()

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
    # executor.start_polling(dp)
    executor.start_webhook(listen="0.0.0.0",
                           port=int(PORT),
                           url_path=TOKEN)
    executor.bot.setWebhook()


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

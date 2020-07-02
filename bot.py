import logging
from urllib.parse import urljoin

import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.webhook import get_new_configured_app
from aiogram.bot import api
import asyncio
from aiohttp import web
import random
from time import sleep

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = 32100
TOKEN = '1359919586:AAG8rzjvD18zcMWJqLg-7Wd6beM1j88i8MY'
bot = Bot(token='1359919586:AAG8rzjvD18zcMWJqLg-7Wd6beM1j88i8MY')
dp = Dispatcher(bot)

WEBHOOK_HOST = 'https://immense-taiga-94950.herokuapp.com/'
WEBHOOK_PATH = '/webhook/' + TOKEN
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 32102

PROJECT_NAME = 'immense-taiga-94950'

WEBHOOK_HOST = f'https://{PROJECT_NAME}.herokuapp.com'  # Enter here your link from Heroku project settings
WEBHOOK_URL_PATH = '/webhook/' + TOKEN
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_URL_PATH

WEBHOOK_URL = urljoin(WEBHOOK_HOST, WEBHOOK_PATH)


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
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


if __name__ == '__main__':
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    app.on_startup.append(on_startup)
    web.run_app(app, host='0.0.0.0', port=os.getenv('PORT'))  # Heroku stores port you have to listen in your app
    # executor.start_polling(dp)

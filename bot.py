import logging
from urllib.parse import urljoin

import os
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.webhook import get_new_configured_app
from aiohttp import web
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.helper import Helper, HelperMode, ListItem

import keyboard as kb

from base_class import StyleTransfer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '1359919586:AAG8rzjvD18zcMWJqLg-7Wd6beM1j88i8MY'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

WEBHOOK_HOST = 'https://immense-taiga-94950.herokuapp.com/'
WEBHOOK_PATH = '/webhook/' + TOKEN
WEBAPP_HOST = '0.0.0.0'

PROJECT_NAME = 'immense-taiga-94950'

WEBHOOK_HOST = f'https://{PROJECT_NAME}.herokuapp.com'  # Enter here your link from Heroku project settings
WEBHOOK_URL_PATH = '/webhook/' + TOKEN
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_URL_PATH
WEBHOOK_URL = urljoin(WEBHOOK_HOST, WEBHOOK_PATH)

DESTINATION_USER_PHOTO = 'pytorch-CycleGAN-and-pix2pix/photo/'


class TestStates(Helper):
    mode = HelperMode.snake_case
    TEST_STATE_0 = ListItem()
    TEST_STATE_1 = ListItem()

state_change_success_message = 'Текущее состояние успешно изменено'
state_reset_message = 'Состояние успешно сброшено'
current_state_message = 'Текущее состояние - "{current_state}", что удовлетворяет условию "один из {states}"'

MESSAGES = {
    'state_change': state_change_success_message,
    'state_reset': state_reset_message,
    'current_state': current_state_message,
}


@dp.message_handler(commands=['help'])
async def send_menu(message: types.Message):
    """отправиь список команд бота"""
    await message.reply(
        text=f"""
        Это StyleTransferBot. Пришлите фотогрфаии\n
        Мои команды: 
        /start -- приветсвенное сообщение
        /help -- увидеть помощь
        /choice -- выбор режима работы бота"""
    )


@dp.message_handler(commands=['choice'])
async def process_command_1(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await message.reply("Выберите тип преобразований", reply_markup=kb.inline_kb)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """отправиь список команд бота"""
    await message.reply("Привет!\nЯ - StyleTransferBot!\nВозможно два режима работы: Style Transfer (перенос стиля) и "
                        "GAN (превращение лошади в зебру).\nДля выбора режима работы введите команду \choice")
    # await send_menu(message=message)


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def process_photo(message: types.Message):
    try:
        filename = 'photo.jpg'
    except Exception as e:
        await bot.send_message(message.from_user.id, f'🤒 Ошибка обработки фотографии: {e}')


@dp.message_handler(state='*', commands=['finish'])
async def process_setstate_command(message: types.Message):
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)
    if not argument:
        await state.reset_state()
        return await message.reply(MESSAGES['state_reset'])

    if (not argument.isdigit()) or (not int(argument) < len(TestStates.all())):
        return await message.reply(MESSAGES['invalid_key'].format(key=argument))

    await state.set_state(TestStates.all()[int(argument)])
    await message.reply(MESSAGES['state_change'], reply=False)


@dp.message_handler(state='*', commands=['setstate'])
@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    await state.reset_state()
    await state.set_state(TestStates.all()[0])
    """argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)"""
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Отправьте две картинки для переноса стиля!')
    # await state.set_state(TestStates.all()[int(argument)])
    # process_photo(callback_query)


@dp.message_handler(state='*', commands=['setstate'])
@dp.callback_query_handler(lambda c: c.data == 'button2')
async def process_callback_button1(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    await state.reset_state()
    await state.set_state(TestStates.all()[1])
    """argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)"""
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Отправьте фотографию лошади!')
    # await state.set_state(TestStates.all()[int(argument)])
    # process_photo(callback_query)
    # await state.reset_state()


@dp.message_handler(state=TestStates.all()[1], content_types=types.ContentTypes.PHOTO)
async def gan(message: types.Message, state: FSMContext):
    await message.answer('GAN начал работу')

    try:
        filename = 'photo.jpg'
        destination = DESTINATION_USER_PHOTO + filename
        os.system("bash pytorch-CycleGAN-and-pix2pix/scripts/download_cyclegan_model.sh horse2zebra")
        await bot.send_message(message.from_user.id, 'Фотография обрабатывается...')
        await message.photo[-1].download(destination=destination)
        os.system("python pytorch-CycleGAN-and-pix2pix/test.py --dataroot 'pytorch-CycleGAN-and-pix2pix/photo' --name "
                  "horse2zebra_pretrained --model test --no_dropout --gpu_ids -1")
        output_path = 'results/horse2zebra_pretrained/test_latest/images/photo_fake.png'
        with open(output_path, 'rb') as photo:
            await bot.send_photo(message.from_user.id, photo)
        os.remove(destination)
        os.remove(output_path)
    except Exception as e:
        await bot.send_message(message.from_user.id, f'🤒 Ошибка обработки фотографии: {e}')

    await message.answer(f"Введите команду /nn для того, чтобы посчитать новую фотографию.")
    await state.finish()


@dp.message_handler(state=TestStates.all()[0], content_types=types.ContentTypes.PHOTO)
async def style_transfer(message: types.Message, state: FSMContext):
    filename = 'content.jpg'
    destination = f'style_transfer/input/{filename}'
    await message.photo[-2].download(destination=destination)

    filename = 'style.jpg'
    destination = f'style_transfer/input/{filename}'
    await message.photo[-1].download(destination=destination)

    await message.answer(f"Обработка изображений")

    result = StyleTransfer()
    output = result.run("style_transfer/input/style.jpg",
                        "style_transfer/input/content.jpg")
    output_path = "style_transfer/output/output.jpg"
    result.save(output_path)
    with open(output_path, 'rb') as photo:
        await bot.send_photo(message.from_user.id, photo)

    await message.answer(f"Введите команду /nn для того, чтобы посчитать новую фотографию.")
    await state.finish()


@dp.message_handler(content_types=types.ContentType.TEXT)
async def style_transfer(message: types.Message):
    text = message.text
    # w = p.model(ll)


async def on_startup(dp):
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


if __name__ == '__main__':
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    app.on_startup.append(on_startup)
    web.run_app(app, host='0.0.0.0', port=os.getenv('PORT'))  # Heroku stores port you have to listen in your app
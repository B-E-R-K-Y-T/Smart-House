# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

# Бот для взаимодействия с сервером

# ----------------------------------------------------------------------------------------------------------------------

import csv
import logging
import base_client
import bot_reg_mode
import bot_authorization_mode
import sys

main_directory = __file__[:str(__file__).rfind('/')]
sys.path.append(main_directory)

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
from parse_files import read_json_file

API_TOKEN = TOKEN

# Configure logging
logging.basicConfig(
    format='%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO
)


# States
class Form(StatesGroup):
    reg_log = State()  # Will be represented in storage as 'Form:reg_log'


storage = MemoryStorage()

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


def get_list_command():
    return [value['command'] for _, value in read_json_file('type_sensors.json')]


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    # if await check_login_user(message):
    #     await check_login_user(message)
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer("Hi!\nI'm smart home mirea bot!")


@dp.message_handler(commands=get_list_command())
async def request_to_server(message: types.Message):
    if await check_login_user(message):
        await send_text_to_server(message)


@dp.message_handler(commands=['status'])
async def get_status_sensor(message: types.Message):
    if await check_login_user(message):
        with open('commands.csv', 'r') as f:
            # Создаем объект DictReader, указываем символ-разделитель ","
            file_reader = csv.DictReader(f, delimiter=",")

            for row in file_reader:
                file_read = row['Command']

            await message.answer('Статус датчика: {0}'.format(file_read[1:]))


@dp.message_handler()
async def echo(message: types.Message):
    if await check_login_user(message):
        await message.reply(message.text)


@dp.message_handler(state=Form.reg_log)
async def registration_or_authorization(message: types.Message, state: FSMContext):
    async with state.proxy():
        data_user = message.text.split(',')

        if len(data_user) != 2:
            await message.answer('Вы ввели данные не правильно! Попробуйте снова.')

            return

        if not await bot_authorization_mode.sign_up(data_user[0], data_user[1]):
            await bot_reg_mode.set_user(data_user[0],
                                        message.from_user.id,
                                        data_user[1])

            await message.answer(f'Вы успешно зарегистрировались!\n\n'
                                 f'Ваш логин: {data_user[0]} и пароль: {data_user[1]}')
            await state.finish()


async def check_login_user(message: types.Message):
    if not await bot_authorization_mode.check_exist_user(message.from_user.id):
        await message.answer('Я вижу Вас впервые. Пожалуйста, зарегистрируйтесь '
                             'или войдите в свой аккаунт!\n\n'
                             'Для этого, просто отправьте мне свой логин и пароль, '
                             'через запятую БЕЗ пробелов.\n\n'
                             'Пример: login,password')
        await Form.reg_log.set()

        return False

    return True


async def send_text_to_server(message: types.Message):
    try:
        client = base_client.Client('127.0.0.1', 8888).get_client()
        client.send(message.text.encode('utf-8'))

        await message.answer('Запрос отправлен корректно.')
    except Exception as e:
        error_msg = f'Path to file with error: <{__file__}>\n\n<CLIENT>: {e}'

        await message.answer(error_msg)
        print(error_msg)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

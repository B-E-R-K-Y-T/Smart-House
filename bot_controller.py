# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

# Бот для взаимодействия с сервером

# ----------------------------------------------------------------------------------------------------------------------

import logging
import base_client
import bot_reg_mode
import bot_authorization_mode

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN

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


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    if await check_login_user(message):
        await check_login_user(message)

        """
        This handler will be called when user sends `/start` or `/help` command
        """
        await message.answer("Hi!\nI'm smart home mirea bot!")


@dp.message_handler(commands=['off', 'on'])
async def request_to_server(message: types.Message):
    if await check_login_user(message):
        try:
            client = base_client.Client('127.0.0.1', 8888).get_client()
            client.send(message.text.encode('utf-8'))

            await message.answer('Запрос отправлен корректно.')
        except Exception as e:
            msg = f'Path to file with error : <{__file__}>\n\n<CLIENT>: {e}'

            await message.answer(msg)
            print(msg)


@dp.message_handler()
async def echo(message: types.Message):
    if await check_login_user(message):
        await message.reply(message.text)


@dp.message_handler(state=Form.reg_log)
async def registration_or_authorization(message: types.Message, state: FSMContext):
    async with state.proxy():
        data_user = message.text.split(',')

        if not await bot_authorization_mode.sign_up(data_user[0], data_user[1]):
            await bot_reg_mode.set_user(data_user[0],
                                        message.from_user.id,
                                        data_user[1])
            # await state.finish()


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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

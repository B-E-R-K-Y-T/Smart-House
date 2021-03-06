# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================


# Бот отправляет запрос на сервак -> выкл свет.
# Сервер должен понять что свет выкл. И добавить эту инфу в
# CSV файл, а бот её оттуда взять и от принтовать в чат
import time
import base_client
import csv
import asyncio
import random

from shm_exceptions import ExceptionErrorCommand

sensor = None


async def read_file():
    while True:
        # try:
        #     sensor = base_client.Client('127.0.0.1', 8888).get_client()
        # except Exception as e:
        #     print(f'<{__file__}>: <CLIENT>: {e}')

        with open('commands.csv', 'r') as f:
            # Создаем объект DictReader, указываем символ-разделитель ","
            file_reader = csv.DictReader(f, delimiter=",")

            for row in file_reader:
                file_read = row['Command']

            if file_read == '/on':
                print('<SENSOR> Temperature = {0}°C'.format(random.randint(15, 25)))
            elif file_read == '/off':
                print("<SENSOR> I'm off!")
            else:
                raise ExceptionErrorCommand('I do not know such a command :(')

        await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(read_file())

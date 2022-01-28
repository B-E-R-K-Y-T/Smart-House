# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================


# Бот отправляет запрос на сервак -> выкл свет.
# Сервер должен понять что свет выкл. И добавить эту инфу в
# CSV файл, а бот её оттуда взять и от принтовать в чат
import os
import sys
import time
import re
import base_client
import csv
import asyncio
import random

main_directory = re.split(r'sensors', str(__file__)[:str(__file__).rfind('/')])[0]
sys.path.append(main_directory)

from shm_exceptions import ExceptionErrorCommand


async def read_file():
    while True:
        # try:
        #     sensor = base_client.Client('127.0.0.1', 8888).get_client()
        # except Exception as e:
        #     print('</ ' + str(__file__) + ' >: <CLIENT>: ' + str(e))

        with open(str(main_directory) + '/commands.csv', 'r') as f:
            # Создаем объект DictReader, указываем символ-разделитель ","
            file_reader = csv.DictReader(f, delimiter=",")

            for row in file_reader:
                file_read = row['Command']

            if file_read == '/on':
                print('<SENSOR> q_1_sensor: Temperature =' + str(random.randint(15, 25)) + '°C')
            elif file_read == '/off':
                print("<SENSOR> q_1_sensor: I'm off!")
            else:
                raise ExceptionErrorCommand('I do not know such a command :(')

        await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(read_file())

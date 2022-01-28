# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

# Скрипт для развертывания проекта.

# ----------------------------------------------------------------------------------------------------------------------

import json
import os


# Разворачивает проект.
def set_smart_house_project():
    with open('code.json', 'r') as js_f:
        dict_json = json.load(js_f)

    for file in dict_json.keys():
        with open(file, 'w') as f:
            f.write(dict_json[file])


# Добавляет файлы датчиков к проекту по запросу.
def add_files():
    sensors = input('Введите типы сенсоров через запятую \n>>>')

    sensors = sensors.replace(' ', '').split(',')

    while True:
        try:
            quality = int(input('Введите кол-во сенсоров \n>>>'))
        except Exception as e:
            print(e)
            continue
        else:
            break
    path_to_file = 'sensors'

    if not os.path.exists(f'{path_to_file}'):
        os.mkdir(f'{path_to_file}')

    # Сборка контейнера.
    for sensor in sensors:
        sensor_copy = sensor

        # Сборка сенсора.
        for i in range(1, quality + 1):
            sensor = sensor_copy + '_' + str(i)

            # Проверка на существование директории.
            if not os.path.exists(f'{path_to_file}/{sensor}'):
                os.mkdir(f'{path_to_file}/{sensor}')

            # Код сенсора.
            with open(f'{path_to_file}/{sensor}/{sensor}.py', 'w') as f:
                f.write(
                    f'''# ======================================================================================================================

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

        with open(str(main_directory) + 'commands.csv', 'r') as f:
            # Создаем объект DictReader, указываем символ-разделитель ","
            file_reader = csv.DictReader(f, delimiter=",")

            for row in file_reader:
                file_read = row['Command']

            if file_read == '/on':
                print('<SENSOR> {sensor}_sensor: Temperature =' + str(random.randint(15, 25)) + '°C')
            elif file_read == '/off':
                print("<SENSOR> {sensor}_sensor: I'm off!")
            else:
                raise ExceptionErrorCommand('I do not know such a command :(')

        await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(read_file())
'''
                )

            # Сборка докер - файлa.
            copying_file(path_to_file, sensor, 'Dockerfile', 'Docker_origin', False)
            # Сборка base_client(ЭТО КОСТЫЛЬ ЕБАНЫЙ СУКА)
            copying_file(path_to_file, sensor, 'base_client.py', 'base_client.py')


# Эта функция работает как обычный replace, только
# позволяет заменять сразу несколько слов в строке
def replace_dict(dict_words: dict, line: str) -> str:
    for old_word, new_word in dict_words.items():
        line = line.replace(old_word, new_word)

    return line


# ЭТА ДЕРЬМОВАЯ ФУНКЦИЯ НУЖНА ДЛЯ КОПИРОВАНИЯ ФАЙЛОВ.
def copying_file(path_to_file, sensor, name_file, new_name_file, flag=True):
    with open(f'{path_to_file}/{sensor}/{name_file}', 'w') as f:
        f.write(
            f'''# ======================================================================================================================

# Project: Smart Home
# Authors: Тимофей Кондаков, Александр Хаметзянов, Полина Зайцева. 

# ======================================================================================================================


'''
        )
        with open(new_name_file) as f_r:
            while True:
                # считываем строку
                line = f_r.readline()
                # прерываем цикл, если строка пустая
                if not line:
                    break

                if not flag:
                    f.write(replace_dict({'sensor': '0'}, line).format(sensor))
                else:
                    f.write(line)


# Развертывание проекта.
switch = input('Выберете режим: добавить(1) или создать(2) \n>>>')

if switch == '2' or switch == 'создать':
    set_smart_house_project()
    add_files()
elif switch == '1' or switch == 'добавить':
    add_files()

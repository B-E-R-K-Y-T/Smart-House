# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

# Скрипт для развертывания проекта.

# ----------------------------------------------------------------------------------------------------------------------

import json
import os
import random


# Разворачивает проект.
def set_smart_house_project():
    with open('../../code.json', 'r') as js_f:
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
    path_to_file = '../../sensors'

    if not os.path.exists(f'{path_to_file}'):
        os.mkdir(f'{path_to_file}')

    list_ports = [0]

    # Сборка контейнера.
    for sensor in sensors:
        sensor_copy = sensor

        # Сборка сенсора.
        for i in range(1, quality + 1):
            sensor = sensor_copy + '_' + str(i)
            port = random.randint(0, 50_000)
            list_ports.append(port)

            # Проверка на существование директории.
            if not os.path.exists(f'{path_to_file}/{sensor}'):
                os.mkdir(f'{path_to_file}/{sensor}')

            # Код сенсора.
            with open(f'{path_to_file}/{sensor}/{sensor}.py', 'w') as f:

                f.write(
                    f'''# ======================================================================================================================

# Project: Smart Home
# Authors: Тимофей Кондаков, Александр Хаметзянов, Полина Зайцева. 

# ======================================================================================================================

import asyncio
import random
import threading

flag = '/on'


def listen_main_server():
    import socket
    global flag
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
    sock.bind(('0.0.0.0', {port}))  # связываем сокет с портом, где он будет ожидать сообщения
    sock.listen(1)  # указываем сколько может сокет принимать соединений
    while True:
        conn, addr = sock.accept()  # начинаем принимать соединения
        print('connected:', addr)  # выводим информацию о подключении
        flag = conn.recv(1024).decode()  # принимаем данные от клиента, по 1024 байт
        print(str(flag))


async def working_sensor():
    while True:
        try:
            if flag == '/on':
                print('<SENSOR> {sensor} ' + str(random.randint(15, 25)) + '°C')
            elif flag == '/off':
                print('<SENSOR> {sensor} Я сплю!')
            else:
                print('<SENSOR> {sensor} Unknown command!')
        except Exception as e:
            print(f'<'+str(__file__)+'>: <SENSOR>: '+str(e))

        await asyncio.sleep(5)


if __name__ == '__main__':
    t = threading.Thread(target=listen_main_server,
                         args=())
    t.start()
    
    asyncio.run(working_sensor())
    
'''
                    )

            # Сборка докер - файлa.
            copying_file(path_to_file, sensor, 'Dockerfile', 'Docker_origin', False)
            # Сборка base_client(ЭТО КОСТЫЛЬ ЕБАНЫЙ СУКА)
            copying_file(path_to_file, sensor, '../tools/base_client.py', 'base_client.py')

    # БЛЯТСКОЕ ГОВНИЩЕ СУКА НАХУЙ БЛЯТЬ ЭТО ГОВНО СУКА НО МНЕ ПОХУЙ УЖЕ(Это порты генерятся.)
    with open(f'../../ports.txt', 'a') as f:
        for port_ in list_ports:
            f.write(str(port_) + ',')


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
    # set_smart_house_project()
    # add_files()
    print('Функция временно вырезана.')
elif switch == '1' or switch == 'добавить':
    add_files()

# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

"""
Типы сенсоров:
    1) Термо-датчик
    2) Датчик освещения
    3) Датчик открытия дверей и окон
    4) Датчик протечки воды
"""

import asyncio
import re

from parse_files import read_json_file
from shm_exceptions import ExceptionTypeSensor
from threading import Thread
from base_sensor import Sensor
from base_data_for_sensor import DataForSensor


# Заглушки
# -------------------------
def get_address():
    """
        Возвращает либо ip адрес либо pin_id
    """
    return '127.0.0.1'


def get_mac_address():
    return '22:F1:55:5D:76:DF'


def get_port():
    return 55000


def get_protocol():
    return 'tcp'
# -------------------------


def replace_dict(dict_words: dict, line: str) -> str:
    for old_word, new_word in dict_words.items():
        line = line.replace(old_word, new_word)

    return line


def get_functions_from_request(request: str) -> list:
    return re.findall(r'(?<=\{).+?(?=\})', request)


async def working_sensor(arg_command: str, arg_to_do: str) -> None:
    while True:
        if message_for_sensor == arg_command:
            function_list = []
            for function in get_functions_from_request(arg_to_do):
                function_list.append(dict_func[function])
            print(
                replace_dict(
                    {key: '' for key in get_functions_from_request(arg_to_do)},
                    arg_to_do)
                .format(*[func() for func in function_list]))
        else:
            print(f'Такой "{message_for_sensor}" команды нет!')

        await asyncio.sleep(1)


# Указать тип сенсора через форматирование файла.
TYPE_SENSOR = '__TYPE_SENSOR__'.lower()
# Указать имя сенсора через форматирование файла.
NAME_SENSOR = '__NAME_SENSOR__'.lower()
# Объект сенсора.
SENSOR = Sensor(get_address(), get_mac_address())
# Указать имя комнаты, в которой стоит сенсор, через форматирование файла.
NAME_ROOM = '__NAME_ROOM__'.lower()
# Сообщения, которые будут отправляться сенсору.
message_for_sensor = None
# Универсальный объект, который генерирует данные для всех типов сенсоров.
data_for_sensor = DataForSensor(name_sensor=NAME_SENSOR,
                                status_network='online',
                                name_room=NAME_ROOM)
# Функционал сенсора:
dict_func = {
    'get_now_date_and_time': data_for_sensor.get_now_date_and_time,
    'get_name_room': data_for_sensor.get_name_room,
    'get_water_in_room': data_for_sensor.get_water_in_room,
    'get_temperature': data_for_sensor.get_temperature,
    'get_status_online': data_for_sensor.get_status_online,
    'get_status_window_switch': data_for_sensor.get_status_window_switch,
    'get_status_door_switch': data_for_sensor.get_status_door_switch,
    'get_status_light_switch': data_for_sensor.get_status_light_switch,
    'get_light_level': data_for_sensor.get_light_level,
}
# Включает(True) и выключает(False) сенсор (ВЫРЕЗАНО)
# switch_sensor = True

# Протокол, на котором работает сеть
PROTOCOL = get_protocol()

if PROTOCOL == 'tcp':
    def send_data_to_sensor():
        import socket
        global message_for_sensor
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
        sock.bind((get_address(), get_port()))  # связываем сокет с портом, где он будет ожидать сообщения
        sock.listen(1)  # указываем сколько может сокет принимать соединений
        while True:
            conn, addr = sock.accept()  # начинаем принимать соединения
            print('connected:', addr)  # выводим информацию о подключении
            message_for_sensor = conn.recv(2048).decode()  # принимаем данные от клиента, по 1024 байт
            if message_for_sensor.startswith('/'):
                # (?<=\/)\w+ - регулярное выражение.
                # Я просто очищаю команду от говна "/" которое телеграмм добавляет.
                message_for_sensor = re.search(r'(?<=\/)\w+', message_for_sensor).group()

if __name__ == '__main__':
    thread = Thread(
        target=send_data_to_sensor,
    )
    thread.start()

    for item in read_json_file('type_sensors.json'):
        type_sensor = item[0]
        command = item[1]['command']
        to_do = item[1]['to_do']

        try:
            description = item[1]['description']
        except KeyError as ke:
            pass

        if TYPE_SENSOR == type_sensor:
            asyncio.run(working_sensor(command, to_do))
            break
        else:
            continue
    else:
        raise ExceptionTypeSensor

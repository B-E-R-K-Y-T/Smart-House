# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================
"""
УЗНАЕТ АЙПИШНИК УСТРОЙСТВА.
import socket
print(socket.gethostbyname(socket.gethostname()))

Типы сенсоров:
    1) Термо-датчик
    2) Датчик освещения
    3) Датчик открытия дверей и окон
    4) Датчик протечки воды
"""

import re
import socket

from utility.database import mongo_api
from datetime import datetime
from config import PATH_TO_TYPE_SNR, IP_SERVER, PORT_SERVER
from config_files.main_config import MONGO_NAME_DB
from utility.tools.parse_files import read_json_file
from utility.tools.static_type import decorate_static_type
from utility.tools.shm_exceptions import TypeSensorException, ErrorProtocolException
from threading import Thread
from utility.sensor.base_sensor import Sensor
from utility.sensor.base_functions_for_sensor import FunctionsForSensor
from characteristics_parser import ConfigReader

config_reader = ConfigReader()

TYPE_SENSOR = config_reader.get_characteristic('type_sensor')

NAME_SENSOR = config_reader.get_characteristic('name_sensor')

NAME_ROOM = config_reader.get_characteristic('name_sensor')

PORT = config_reader.get_characteristic('port')

PROTOCOL = config_reader.get_characteristic('main_protocol').upper()

MAC_ADDRESS = config_reader.get_characteristic('address')['mac_address']


# Заглушки
# -------------------------
def get_address():
    """
        Возвращает либо ip-адрес либо pin_id
    """

    # return socket.gethostbyname(socket.gethostname())
    if PROTOCOL != 'ПРОТОКОЛУ В КОТОРОМ ЕСТЬ PIN_ID':
        ip_v4 = config_reader.get_characteristic('address').get('ip_v4')
        ip_v6 = config_reader.get_characteristic('address').get('ip_v6')

        return ip_v4 if ip_v4 and ip_v4 != 'PASS' else ip_v6
    else:
        return config_reader.get_characteristic('address')['pin_id']

# -------------------------


@decorate_static_type
def replace_dict(dict_words: dict, line: str) -> str:
    for old_word, new_word in dict_words.items():
        line = line.replace(old_word, new_word)

    return line


@decorate_static_type
def get_functions_from_request(request: str) -> list:
    # (?<=\{).+?(?=\}) - регулярное выражение
    # Нахожу все вхождения в строку по сигнатуре: '{что-то написано}'
    return re.findall(r'(?<=\{).+?(?=\})', request)


@decorate_static_type
def logging(data: str):
    with open(file='log.txt', mode='a') as log_file:
        log_file.write(f'{datetime.now().strftime("Дата: %d/%m/%Y  Время: %H:%M:%S")} '
                       f'PROTOCOL = {PROTOCOL}\n\t'
                       f'TYPE_SENSOR = {TYPE_SENSOR}\n\t'
                       f'NAME_SENSOR = {NAME_SENSOR}\n\t'
                       f'NAME_ROOM = {NAME_ROOM}\n\t'
                       f'PORT = {PORT}\n\t'
                       f'MAC_ADDRESS = {MAC_ADDRESS} : => '
                       f'\n\t\t{data}\n\n')


def write_logs(data=None):
    """
        Эта функция записывает логи сенсора в бд
    """
    collection = mongo_db[f'{TYPE_SENSOR}_{NAME_SENSOR}']
    log = {
        'DATA': data,
        'NAME_SENSOR': NAME_SENSOR,
        'TYPE_SENSOR': TYPE_SENSOR,
        'DATE_TIME': datetime.now().strftime("Дата: %d/%m/%Y  Время: %H:%M:%S"),
        'NAME_ROOM': NAME_ROOM,
        'PROTOCOL': PROTOCOL
    }

    try:
        collection.insert_one(log)
        # collection.update_one(log)
    except Exception as e:
        logging(f'{repr(e)}')


@decorate_static_type
def working_sensor(arg_commands: dict, message_for_sensor: str):
    for name_command, structure_command in arg_commands.items():
        if message_for_sensor == name_command:
            to_do = structure_command['to_do']
            if message_for_sensor.startswith('config_'):
                args = structure_command['args'].replace(' ', '').split(',')
                dict_func[to_do](*args)
                break
            elif message_for_sensor.startswith('f_'):
                pass
            else:
                # Парсинг строки json-файла. Достаю оттуда все названия функций и храню
                # ссылки на них в списке function_list
                # Проще говоря, преобразовываю функции из json файла
                # в функции из FunctionsForSensor.
                function_list = []
                for function in get_functions_from_request(to_do):
                    function_list.append(dict_func[function])
                # Форматирую строку: создаю словарь названий функций. С помощью
                # функции replace_dict удаляю их, но оставляю после них такой
                # шаблон {} для метода .format в котором распаковываю список
                # значений функций в том же порядке, в котором они стояли в исходной
                # строке, тем самым я "вызвал" эти функции в json-файле.
                # Надеюсь, что понятно описал...
                result = replace_dict(
                    {key: '' for key in get_functions_from_request(to_do)}, to_do).format(
                    *[func() for func in function_list])
                print(result)
                logging(f'Результат запроса от пользователя: {result}')
                write_logs(result)
                break
    else:
        if message_for_sensor is not None:
            print(f'Такой "{message_for_sensor}" команды нет!')
            logging(f'Такой "{message_for_sensor}" команды нет!')
            write_logs(f'Такой "{message_for_sensor}" команды нет!')


SENSOR = Sensor(get_address(), MAC_ADDRESS)
# Сообщения, которые будут отправляться сенсору.
message_for_sensor = None
# Универсальный объект, который генерирует данные для всех типов сенсоров.
functions_for_sensor = FunctionsForSensor(name_sensor=NAME_SENSOR,
                                          status_network='online',
                                          name_room=NAME_ROOM)
# База данных
mongo_db = mongo_api.MongoSH().get_mongo_object()[MONGO_NAME_DB]
# Функционал сенсора:
dict_func = {
    'get_now_date_and_time': functions_for_sensor.get_now_date_and_time,
    'get_name_room': functions_for_sensor.get_name_room,
    'get_water_in_room': functions_for_sensor.get_water_in_room,
    'get_temperature': functions_for_sensor.get_temperature,
    'get_status_online': functions_for_sensor.get_status_online,
    'get_status_window_switch': functions_for_sensor.get_status_window_switch,
    'get_status_door_switch': functions_for_sensor.get_status_door_switch,
    'get_status_light_switch': functions_for_sensor.get_status_light_switch,
    'get_light_level': functions_for_sensor.get_light_level,
    'set_status_network': functions_for_sensor.set_status_network,
    'set_status_door_switch': functions_for_sensor.set_status_door_switch,
    'set_status_light_switch': functions_for_sensor.set_status_light_switch,
    'set_name_room': functions_for_sensor.set_name_room,
    'set_water_in_room': functions_for_sensor.set_water_in_room,
}
# Протокол, на котором работает сеть
if PROTOCOL == 'TCP':
    # TODO: перенести реализацию для каждого протокола либо в отдельный класс, либо в модуль
    def send_data_to_sensor():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
        sock.bind((get_address(), PORT))  # связываем сокет с портом, где он будет ожидать сообщения
        sock.listen(1)  # указываем сколько может сокет принимать соединений
        while True:
            conn, addr = sock.accept()  # начинаем принимать соединения
            print(f'connected: {addr}')  # выводим информацию о подключении
            logging('connected: addr') # выводим информацию о подключении
            message_for_sensor = conn.recv(2048).decode()  # принимаем данные от клиента, по 1024 байт
            if message_for_sensor.startswith('/'):
                # (?<=\/)\w+ - регулярное выражение.
                # Я просто очищаю команду от говна "/" которое телеграмм добавляет.
                message_for_sensor = re.search(r'(?<=\/)\w+', message_for_sensor).group()

            for type_sensor, commands in read_json_file(PATH_TO_TYPE_SNR):
                if TYPE_SENSOR == type_sensor:
                    working_sensor(commands, message_for_sensor)
                    break
                else:
                    continue
            else:
                raise TypeSensorException()

elif PROTOCOL == 'MQTT':
    raise Exception()
elif PROTOCOL == 'AQMP':
    raise Exception()
elif PROTOCOL == 'COAP':
    raise Exception()
elif PROTOCOL == 'UDP':
    raise Exception()
elif PROTOCOL == 'HTTP':
    raise Exception()
else:
    raise ErrorProtocolException()

if __name__ == '__main__':
    thread = Thread(
        target=send_data_to_sensor,
    )
    thread.start()

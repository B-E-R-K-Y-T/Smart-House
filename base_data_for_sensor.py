# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# Температура, открытие, закрытие открытие дверей, вкл выкл свет, в случае протечки: замыкание или размыкание
# Статус: онлайн и оффлайн,
# уровень света, открыто или закрыто окно, время суток, время года.
# TODO: Добавить кондиционеры, печку

import random
import shm_exceptions

from datetime import datetime


# Обычная заглушка для значений
_PASS = 'PASS'


class DataForSensor:
    def __init__(self, *, name_sensor, status_network, name_room,
                 temperature='10', status_door_switch='close', status_light_switch='off',
                 status_window_switch='close', status_light_level_switch='0', status_water=False):
        self.name_sensor = name_sensor
        self.status_network = status_network
        self.name_room = name_room
        self.temperature = temperature
        self.status_door_switch = status_door_switch
        self.status_light_switch = status_light_switch
        self.status_window_switch = status_window_switch
        self.status_light_level_switch = status_light_level_switch
        self.status_water = status_water
        self._check_status_network()

    def _check_status_network(self):
        if self.status_network == 'online':
            return True
        elif self.status_network == 'offline':
            return False
        else:
            raise shm_exceptions.ExceptionOnlineStatus

    def _get_status_network(self):
        if self._check_status_network():
            return {'bool': True, 'info': 'Доступ есть!'}
        else:
            return {'bool': False, 'info': 'Не могу получить доступ!'}

    def _now_hour(self):
        return datetime.now().time().hour

    def _get_sub_time_range(self, start, end):
        return str(list(range(start, end)))

    def get_now_date_and_time(self):
        if self._get_status_network()['bool']:
            return f'Текущая дата и время = {datetime.now().strftime("Дата: %d/%m/%Y  Время: %H:%M:%S")}'
        else:
            return self._get_status_network()['info']

    def get_name_room(self):
        if self._get_status_network()['bool']:
            return self.name_room
        else:
            return self._get_status_network()['info']

    def get_water_in_room(self):
        if self._get_status_network()['bool']:
            return self.status_water
        else:
            return self._get_status_network()['info']

    def get_temperature(self):
        """
            Возвращает температуру в комнате в зависимости от времени суток.
        """
        if self._get_status_network()['bool']:
            time_range_with_temperature = {
                self._get_sub_time_range(0, 6): random.randint(-1, 5),
                self._get_sub_time_range(6, 10): random.randint(13, 20),
                self._get_sub_time_range(10, 16): random.randint(20, 30),
                self._get_sub_time_range(16, 20): random.randint(15, 20),
                self._get_sub_time_range(20, 24): random.randint(5, 10),
            }
            temperature = self.temperature
            koef_temperature = 10

            for key in time_range_with_temperature:
                if str(self._now_hour()) in key:
                    temperature = time_range_with_temperature[key]
                    break

            return temperature + koef_temperature
        else:
            return self._get_status_network()['info']

    def get_status_online(self):
        return self.status_network

    def get_status_window_switch(self):
        if self._get_status_network()['bool']:
            return self.status_window_switch
        else:
            return self._get_status_network()['info']

    def get_status_door_switch(self):
        if self._get_status_network()['bool']:
            return self.status_door_switch
        else:
            return self._get_status_network()['info']

    def get_status_light_switch(self):
        if self._get_status_network()['bool']:
            return self.status_light_switch
        else:
            return self._get_status_network()['info']

    def get_light_level(self):
        """
            Возвращает уровень освещенности в комнате в зависимости от того, открыло ли окно, открыта ли дверь и
            включен ли свет?
        """
        if self._get_status_network()['bool']:
            koef_light_level = random.randint(5, 10)
            result_list = [koef_light_level]

            for item in [self.status_light_switch, self.status_door_switch, self.status_window_switch]:
                if 'on' in item or 'open' in item:
                    result_list.append(random.randint(10, 30))

            return sum(result_list)
        else:
            return self._get_status_network()['info']

    def set_status_network(self, new_status_network):
        self.status_network = new_status_network

    def set_status_door_switch(self, status_window_switch):
        if self._get_status_network()['bool']:
            self.status_window_switch = status_window_switch
        else:
            print(self._get_status_network()['info'])

    def set_status_light_switch(self, status_light_switch):
        if self._get_status_network()['bool']:
            self.status_light_switch = status_light_switch
        else:
            print(self._get_status_network()['info'])

    def set_name_room(self, name_room):
        if self._get_status_network()['bool']:
            self.name_room = name_room
        else:
            print(self._get_status_network()['info'])

    def set_water_in_room(self, status_water):
        if self._get_status_network()['bool']:
            self.status_water = status_water
        else:
            print(self._get_status_network()['info'])


if __name__ == '__main__':
    # Тестовый код
    dfs = DataForSensor(name_sensor='test_sensor', status_network='offline', name_room='Спальня')
    print('Вывод без подключения к сети: ')
    print(dfs.get_temperature())

    dfs.set_status_network('online')
    print('Вывод c подключением к сети: ')

    print(dfs.get_temperature())
    print(dfs.get_light_level())
    print(dfs.get_now_date_and_time())
    print(dfs.get_name_room())
    print(dfs.get_status_door_switch())
    print(dfs.get_status_light_switch())
    print(dfs.get_status_window_switch())
    print(dfs.get_status_online())

    dfs.set_status_network('offline')
    print('Вывод без подключения к сети: ')

    print(dfs.get_temperature())
    print(dfs.get_light_level())
    print(dfs.get_now_date_and_time())
    print(dfs.get_name_room())
    print(dfs.get_status_door_switch())
    print(dfs.get_status_light_switch())
    print(dfs.get_status_window_switch())
    print(dfs.get_status_online())

    dfs.set_status_network('online')
    dfs.set_status_door_switch('open')
    dfs.set_status_light_switch('on')
    print(dfs.get_light_level())

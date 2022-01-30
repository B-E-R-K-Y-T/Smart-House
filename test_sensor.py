# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================


# Бот отправляет запрос на сервак -> выкл свет.
# Сервер должен понять что свет выкл. И добавить эту инфу в
# CSV файл, а бот её оттуда взять и от принтовать в чат
import base_client
import asyncio
import random
import threading

flag = '/on'


def listen_main_server():
    import socket
    global flag
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
    sock.bind(('', 55000))  # связываем сокет с портом, где он будет ожидать сообщения
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
                print('<SENSOR> {0}°C'.format(random.randint(15, 25)))
            elif flag == '/off':
                print('<SENSOR> Я сплю!')
            else:
                print('Unknown command!')
        except Exception as e:
            print(f'<{__file__}>: <SENSOR>: {e}')

        await asyncio.sleep(5)


if __name__ == '__main__':
    t = threading.Thread(target=listen_main_server,
                         args=())
    t.start()

    asyncio.run(working_sensor())

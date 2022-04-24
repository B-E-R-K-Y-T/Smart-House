# ======================================================================================================================

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
    sock.bind(('0.0.0.0', 18725))  # связываем сокет с портом, где он будет ожидать сообщения
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
                print('<SENSOR> rr_1 ' + str(random.randint(15, 25)) + '°C')
            elif flag == '/off':
                print('<SENSOR> rr_1 Я сплю!')
            else:
                print('<SENSOR> rr_1 Unknown command!')
        except Exception as e:
            print(f'<'+str(__file__)+'>: <SENSOR>: '+str(e))

        await asyncio.sleep(5)


if __name__ == '__main__':
    t = threading.Thread(target=listen_main_server,
                         args=())
    t.start()
    
    asyncio.run(working_sensor())
    

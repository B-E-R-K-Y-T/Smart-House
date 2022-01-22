# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================


# Бот отправляет запрос на сервак -> выкл свет.
# Сервер должен понять что свет выкл. И добавить эту инфу в
# CSV файл, а бот её оттуда взять и от принтовать в чат

import base_client
import base_server


# try:
#     sensor = base_client.Client('127.0.0.1', 8888).get_client()
# except Exception as e:
#     print(f'<{__file__}>: <CLIENT>: {e}')
# try:
#     server = base_server.Server('127.0.0.1', 2323)
# except Exception as e:
#     print(f'<{__file__}>: <SERVER>: {e}')


while True:
    try:
        sensor = base_client.Client('127.0.0.1', 8888).get_client()
    except Exception as e:
        print(f'<{__file__}>: <CLIENT>: {e}')
    try:
        sensor.send(input('Enter: ').encode('utf-8'))
    except BrokenPipeError as e:
        print(f'{e}')
    data = sensor.recv(1024)
    if not data:
        continue
    print(data)
    # sensor.send(data.upper())




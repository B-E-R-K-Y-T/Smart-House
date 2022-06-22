# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

import socket


# noinspection PyGlobalUndefined
class Client:
    client = None

    def __init__(self, ip: str, port: int):
        global client

        client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        client.connect((ip, port))

    @staticmethod
    def get_client():
        global client
        return client

    @staticmethod
    def send_msg(data: str):
        global client
        client.send(data.encode('utf-8'))
        print('Запрос отправлен.')

    @staticmethod
    def recv_msg(bufsize=1024):
        global client
        return client.recv(bufsize)

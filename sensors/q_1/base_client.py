# ======================================================================================================================

# Authors: BERKYT

# ======================================================================================================================


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

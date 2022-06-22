# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

# Базовый класс сервера

# ----------------------------------------------------------------------------------------------------------------------

import asyncio

from utility.tools.shm_exceptions import ExceptionErrorProtocol
from utility.tools.shm_protocols import TCPServerProtocol


class Server(TCPServerProtocol):
    def __init__(self, host, port, protocol='TCP'):
        print(f'<SERVER>: '
              f'Address: {host}; '
              f'Port: {port}; '
              f'Protocol: {protocol} '
              f'Status: Activating...')
        asyncio.run(self.start_server(host, port, protocol))

    @staticmethod
    async def start_server(host, port, protocol):
        loop = asyncio.get_running_loop()

        protocols = {'MQTT': '',
                     'AQMP': '',
                     'COAP': '',
                     'TCP': TCPServerProtocol(),
                     'udp': '',
                     'http': ''}

        for prot in protocols.keys():
            if protocol == prot and protocols[prot]:
                server = await loop.create_server(
                    lambda: protocols[prot],
                    host, port)

                break
        else:
            raise ExceptionErrorProtocol('I do not know such a protocol :(')

        async with server:
            # Метод Server.serve_forever() начинает принимать
            # подключения, пока сопрограмма не будет отменена.
            # Отмена задачи serve_forever приводит к закрытию сервера.
            #
            # Представляет собой сопрограмму.
            #
            # Этот метод можно вызвать, если сервер уже принимает
            # соединения. На один объект Server может существовать
            # только одна задача Server.serve_forever().
            await server.serve_forever()

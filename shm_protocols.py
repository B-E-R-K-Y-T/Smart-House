# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

# Тут будут лежать реализации протоколов.

# ----------------------------------------------------------------------------------------------------------------------

import asyncio
import parse_files
import os
import csv


# TCP протокол
# ----------------------------------------------------------------------------------------------------------------------
class TCPServerProtocol(asyncio.Protocol):
    # Вызывается если соединение с сервером было
    # установлено!
    def connection_made(self, transport):
        # transport как я понял это
        # объект соединения
        peername = transport.get_extra_info('peername')
        print('<SERVER>: Connection from {}'.format(peername))
        # Ссылка на transport.
        self.transport = transport

    # Called when some data is received.
    # The argument is a bytes object.
    def data_received(self, data):
        message = data.decode()
        # Проверка на существование файла 'commands.csv'. Если его не будет - создать.
        if not os.path.exists('commands.csv'):
            with open('commands.csv', 'w') as f:
                names = ["Address", "Command"]
                file_writer = csv.DictWriter(f, delimiter=",",
                                             lineterminator="\r", fieldnames=names)

                file_writer.writeheader()

        # Запись запроса от бота на сервере в csv - файл
        with open('commands.csv', 'a') as f:
            names = ["Address", "Command"]
            file_writer = csv.DictWriter(f, delimiter=",",
                                         lineterminator="\r", fieldnames=names)

            file_writer.writerow({names[0]: self.transport.get_extra_info('peername'),
                                  names[1]: data.decode()})

        print('<SERVER>: Data received: {!r}'.format(message))

        print('<SERVER>: Send: {!r}'.format(message))
        self.transport.write(data)

        print('<SERVER>: Close the client socket')
        # Закрывает соединение после того, как получит
        # Какой - то запрос.
        self.transport.close()

    def connection_lost(self, exc):
        print('<SERVER>: Connection with {} is lost!'.format(self.transport.
                                                             get_extra_info('peername')))
# ----------------------------------------------------------------------------------------------------------------------

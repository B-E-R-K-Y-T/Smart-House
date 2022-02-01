# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

# Тут будут лежать реализации протоколов.

# ----------------------------------------------------------------------------------------------------------------------

import asyncio
import parse_files
import csv
import base_client

clients = []


# TCP протокол
# ----------------------------------------------------------------------------------------------------------------------
class TCPServerProtocol(asyncio.Protocol):
    # Вызывается если соединение с сервером было
    # установлено!
    def connection_made(self, transport):
        clients.append(transport.get_extra_info('peername'))

        # transport как я понял это
        # объект соединения
        peername = transport.get_extra_info('peername')
        print('<SERVER>: Connection from {}'.format(peername))
        # Ссылка на transport.
        self.transport = transport

    # Called when some data is received.
    # The argument is a bytes object.
    def data_received(self, data):
        print(f'Path to file with: <{__file__}>\n\n<SERVER>: Packages received.')

        message = data.decode()
        # self.transport.write(('Echoed back: {}'.format(message)).encode())
        # data_client = websockets.recv()

        # print(data_client)

        with open('ports.txt', 'r') as f:
            for port in str(f.read()).split(','):
                print('message = ' + message)

                try:
                    client = base_client.Client('127.0.0.1', int(port)).get_client()
                    client.send(message.encode('utf-8'))
                except Exception as e:
                    error_msg = f'Path to file with error: <{__file__}>\n\n<SERVER>: {e}'
                    print(error_msg)
                    continue

        # Проверка на существование файла 'commands.csv'. Если его не будет - создать.
        parse_files.create_csv_file_if_not_exists('commands.csv')

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
        print(clients)
        self.transport.close()

    def connection_lost(self, exc):
        clients.remove(self.transport.get_extra_info('peername'))
        print('<SERVER>: Connection with {} is lost!'.format(self.transport.
                                                             get_extra_info('peername')))
# ----------------------------------------------------------------------------------------------------------------------

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
import requests

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from http.server import CGIHTTPRequestHandler


# TCP протокол
# ----------------------------------------------------------------------------------------------------------------------
clients = []


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


# HTTP протокол
# ----------------------------------------------------------------------------------------------------------------------

# TODO: Сделать так, чтобы этот протокол принимал запросы от Егора.
class Http:
    class State:
        @staticmethod
        def test():
            return 1

    class HttpGetHandler(BaseHTTPRequestHandler):
        """Обработчик с реализованным методом do_GET."""

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET")
            self.end_headers()
            self.wfile.write('ПОШЕЛ НАХУЙ'.encode())
            self.wfile.write('ПРОЕКТ - ГОВНО!'.encode())

    def request_post(self, address, data):
        requests.post(address, data=data)

    def run(self, server_class=HTTPServer, handler_class=HttpGetHandler):
        server_address = ('192.168.1.69', 3000)
        httpd = server_class(server_address, handler_class)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    h = Http()
    h.run()

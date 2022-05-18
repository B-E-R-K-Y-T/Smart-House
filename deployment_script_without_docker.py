# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

# Скрипт для развертывания проекта.

# ----------------------------------------------------------------------------------------------------------------------

import parse_files
import requests
import random

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer


class Http:
    class HttpGetHandler(BaseHTTPRequestHandler):
        """Обработчик с реализованным методом do_GET."""

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET")
            self.end_headers()
            name, type_sensor = create_sensor()
            request = f'"["name": "{name}", "type_sensor": "{type_sensor}"]"'
            request = request.replace('[', '{').replace(']', '}')
            self.wfile.write(request.encode())

    def request_post(self, address, data):
        requests.post(address, data=data)

    def run(self, server_class=HTTPServer, handler_class=HttpGetHandler):
        server_address = ('192.168.1.69', 3000)
        httpd = server_class(server_address, handler_class)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()


def create_sensor():
    name = f'name_{random.randint(10,10_000)}'
    type_sensor = 'temperature_sensor'
    parse_files.create_folder_if_not_exists(f'sensors/{name}')
    with open(f'sensors/{name}/{name}.py', 'w') as sensor_file:
        for line in parse_files.read_file('base_realization_sensor.py'):
            sensor_file.write(line)

    return name, type_sensor


if __name__ == '__main__':
    h = Http()
    h.run()


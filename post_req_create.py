import random

from flask import Flask, jsonify, request

import parse_files

app = Flask(__name__)


@app.route('/create_sensor', methods=['POST'])
def create_sensor():
    # ЗАЕБАЛО
    dict_data_of_sensor = dict(request.get_json(force=True))
    print(type(dict_data_of_sensor))
    print(dict_data_of_sensor)

    name = dict_data_of_sensor['name']
    type_sensor = dict_data_of_sensor['type_sensor']
    parse_files.create_folder_if_not_exists(f'sensors/{name}')
    with open(f'sensors/{name}/{name}.py', 'w') as sensor_file:
        for line in parse_files.read_file('base_realization_sensor.py'):
            line = line.replace('__TYPE_SENSOR__', type_sensor)
            sensor_file.write(line)

    with open(f'sensors/{name}/type_sensors.json', 'w') as json_file:
        for line in parse_files.read_file('type_sensors.json'):
            json_file.write(line)

    return jsonify(request.get_json(force=True))


from flask import Flask, jsonify, request

app = Flask(__name__)

main_directory = __file__[:str(__file__).rfind('/')]
print(f'{main_directory}/sensors/sensors/sensors.py')


@app.route('/create_sensor', methods=['POST'])
def create_sensor():
    # Запускать файл так в терминале: FLASK_APP=post_req_create.py flask run -h 192.168.1.69 -p 3000
    # Пинговать его так: curl --request POST --header 'Content-Type: application/json' --data '{"name": "value", "type_sensor": "temperature_sensor"}' 'http://192.168.1.69:3000/create_sensor'

    dict_data_of_sensor = dict(request.get_json(force=True))
    print(type(dict_data_of_sensor))
    print(dict_data_of_sensor)

    #РАБОТАЕТ!!!!!
    resp = app.make_response(jsonify(request.get_json(force=True)))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

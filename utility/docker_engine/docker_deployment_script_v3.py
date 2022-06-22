# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

# Скрипт для развертывания проекта.

# ----------------------------------------------------------------------------------------------------------------------

import re
from utility.tools import parse_files

# -create -sensor[-path /home/berkyt/PycharmProjects/smart_home/sensors/e_1; -name name; -type type; -protocol protocol; -name_room name_room;];;
# -edit -type

dict_commands = {
    '-create': {
        '-sensor': ['-path', '-name', '-type', '-protocol'],
        '-file': ['-path', '-name', '-content'],
    },
}


def get_create(line):
    return re.search(r'(?<=-create).+(?=\;)', line).group()


def get_edit_type(line):
    return re.search(r'(?<=-edit_type).+(?=\;)', line).group()


def get_for_do(line):
    try:
        return int(re.search(r'(?<=-for)[0-9]+(?=do)', line).group())
    except:
        return 1


def get_file(line):
    return re.search(r'(?<=-file\[).+?(?=\]\;)', line).group()


def get_sensor(line):
    return re.search(r'(?<=-sensor\[).+?(?=\]\;)', line).group()


def get_path(line):
    return re.search(r'(?<=-path).+?(?=\;)', line).group()


def get_name(line):
    return re.search(r'(?<=-name).+?(?=\;)', line).group()


def get_type(line):
    return re.search(r'(?<=-type).+?(?=\;)', line).group()


def get_protocol(line):
    return re.search(r'(?<=-protocol).+?(?=\;)', line).group()


def get_name_room(line):
    return re.search(r'(?<=-name_room).+?(?=\;)', line).group()


def get_content(line):
    return re.search(r'(?<=-content).+?(?=\;)', line).group()


def create_sensor(*, path_sensor, name_sensor, type_sensor, protocol_sensor, name_room):
    with open(f'{path_sensor}/{name_sensor}', mode='a') as file_sensor:
        for line in parse_files.read_file('../sensor/base_realization_sensor.py'):
            line = parse_files.replace_dict({'__TYPE_SENSOR__': type_sensor,
                                             '__PROTOCOL__': protocol_sensor,
                                             '__NAME_SENSOR__': name_sensor,
                                             '__NAME_ROOM__': name_room}, line)
            file_sensor.write(line)


def create_file(path, name, content):
    with open(f'{path}/{name}', mode='w') as file:
        file.write(content)


def edit_json():
    pass


def interpreter(request):
    if request[-1] != ';':
        raise Exception('Syntax error: at the end it was expected ";"')
    else:
        if request.startswith('-create'):
            request = get_create(request)
            if request.startswith('-sensor'):
                create_sensor(path_sensor=get_path(request),
                              name_sensor=get_name(request),
                              type_sensor=get_type(request),
                              protocol_sensor=get_protocol(request),
                              name_room=get_name_room(request))
                print('Successfully.')
            if request.startswith('-file'):
                create_file(name=get_name(request),
                            path=get_path(request),
                            content=get_content(request))
                print('Successfully.')
        if request.startswith('-edit_type'):
            request = get_edit_type(request)


def listening_input():
    while True:
        line = input('>>>')
        if line == '-exit':
            print('Successfully.')
            break
        interpreter(line.replace(' ', ''))


if __name__ == '__main__':
    listening_input()

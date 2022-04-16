# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

# Скрипт для развертывания проекта.

# ----------------------------------------------------------------------------------------------------------------------
import json
import os
import static_type
import parse_files
import shm_exceptions


@static_type.decorate_static_type
def create_path_if_not_found(path_to_file: str) -> str:
    if not os.path.exists(f'{path_to_file}'):
        os.mkdir(f'{path_to_file}')

        return path_to_file


def converting_types(var, class_type):
    while True:
        try:
            var = class_type(var)
        except ValueError as e:
            var = input(f'Ошибка: {e}\nПопробуйте снова! \n>>>')
            continue
        else:
            return var


@static_type.decorate_static_type
def checking_exist_file(path_to_file: str) -> str:
    if not os.path.exists(f'{path_to_file}'):
        raise FileExistsError(f'Path: "{path_to_file}" does not exist!')
    else:
        return path_to_file


# Разворачивает проект.
def set_smart_house_project() -> None:
    with open('code.json', 'r') as js_f:
        dict_json = json.load(js_f)

    for file in dict_json.keys():
        with open(file, 'w') as f:
            f.write(dict_json[file])


# Эта функция работает как обычный replace, только
# позволяет заменять сразу несколько слов в строке
@static_type.decorate_static_type
def replace_dict(dict_words: dict, line: str) -> str:
    for old_word, new_word in dict_words.items():
        line = line.replace(old_word, new_word)

    return line


@static_type.decorate_static_type
def interpreter_file(path_to_file: str, path_to_save: str, dict_operators: dict, name_file: str) -> None:
    with open(f'{path_to_save}/{name_file}', 'w') as write_file:
        for read_file in reading_file(path_to_file):
            write_file.write(replace_dict(dict_operators, read_file))


@static_type.decorate_static_type
def reading_file(path_to_file: str) -> str:
    with open(path_to_file, 'r') as read_file:
        for line in read_file:
            yield line


# TODO: Переписать эту функцию, чтобы она выглядела по-человечески.
@static_type.decorate_static_type
def create_docker_files(dict_paths_to_docker_file: dict) -> None:
    for key, value in dict_paths_to_docker_file.items():
        if str(key).lower().startswith('docker'):
            interpreter_file(value[0], dict_paths_to_docker_file['path_to_save'],
                             value[1],
                             value[2], )


# TODO: Переписать эту функцию, чтобы она выглядела по-человечески.
def create_sensor_files(dict_paths: dict) -> None:

    interpreter_file(dict_paths['sensor_file_base']['path_to_base_sensor'],
                     dict_paths['path_to_save'],
                     dict_paths['sensor_file_base']['dict_replace'],
                     dict_paths['sensor_file_base']['name_file'])


def add_files() -> None:
    def get_replace_dict() -> dict:
        quality_operators = converting_types(input('\tВведите кол-во операторов которые меняем \n\t>>>'), int)
        dict_operators = {

        }

        for _ in range(quality_operators):
            old_operator = input('\t\tЧто заменить? \n\t\t>>>')
            dict_operators[old_operator] = input('\t\tНа что заменить? \n\t\t>>>')

        return dict_operators

    dict_paths = {

    }

    sensors = input('Введите типы сенсоров через запятую \n>>>')
    sensors = sensors.replace(' ', '').split(',')
    quality = converting_types(input('Введите кол-во сенсоров \n>>>'), int)

    dict_paths['docker_file'] = (checking_exist_file(
        input('Введите путь до базового докер файла \n>>>')), get_replace_dict(),
        input('Введите название файла \n>>>'))

    dict_paths['docker_file_compose'] = (checking_exist_file(
        input('Введите путь до базового докер к. файла \n>>>')), get_replace_dict(),
        input('Введите название файла \n>>>'))

    dict_paths['sensor_file_base'] = {'path_to_base_sensor': checking_exist_file(
        input('Введите путь до базового файла сенсора \n>>>')), 'dict_replace': get_replace_dict(),
        'name_file': input('Введите название файла \n>>>')}

    dict_paths['path_to_save'] = create_path_if_not_found(
        input('Введите путь сохранения файлов \n>>>'))

    print('Paths: ', dict_paths)
    create_docker_files(dict_paths)
    # TODO: ДОДЕЛАТЬ ЭТУ ФУНКЦИЮ И ВСЕ БУДЕТ ГОТОВО!
    print(dict_paths['sensor_file_base'])


    # create_sensor_files(dict_paths['sensor_file_base'][0],
    #                     dict_paths['sensor_file_base'][1],
    #                     dict_paths['sensor_file_base'][2])


def main():
    # Развертывание проекта.
    while True:
        switch = input('Выберете режим: добавить(1), создать(2) или выйти(-1) \n>>>')
        switch = switch.lower()

        if switch == '2' or switch == 'создать':
            # print('Разворачиваю проект...')
            # set_smart_house_project()
            # print('Создание первичных датчиков: ')
            # add_files()
            print('Функция временно вырезана.')
        elif switch == '1' or switch == 'добавить':
            add_files()
        elif switch == '-1' or switch == 'выход':
            break
        else:
            print('Вы ввели несуществующую команду! Попробуйте ещё раз: \n')


if __name__ == '__main__':
    main()

# 0 ('docker_file', ('Введите путь до базового докер файла ', {'Что заменить? ': 'На что заменить? '}, 'Docker.txt'))

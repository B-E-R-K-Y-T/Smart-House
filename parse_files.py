# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

# API для работы с файлами

# ----------------------------------------------------------------------------------------------------------------------

import os
import csv
import codecs
import json


# TODO: ЭТА ФУНКЦИЯ НЕ РАБОТАЕТ. ДОДЕЛАТЬ ПОТОМ!
async def write_data_to_file(data, file):
    # Проверка на существование файла 'commands.csv'. Если его не будет - создать.
    if not os.path.exists(file):
        with open(file, 'w') as f:
            names = ["Address", "Command"]
            file_writer = csv.DictWriter(f, delimiter=",",
                                         lineterminator="\r", fieldnames=names)

            file_writer.writeheader()

    # Запись запроса от бота на сервере в csv - файл
    with open(file, 'a') as f:
        names = ["Address", "Command"]
        file_writer = csv.DictWriter(f, delimiter=",",
                                     lineterminator="\r", fieldnames=names)

        # file_writer.writerow({names[0]: self.transport.get_extra_info('peername'),
        #                       names[1]: data.decode()})


async def create_csv_file_if_not_exists_async(loc_name_file, names=None):
    if names is None:
        names = ["Login", "ID", "Password"]
    # Проверка на существование файла 'reg_user.csv'. Если его не будет - создать.
    if not os.path.exists(loc_name_file):
        with open(loc_name_file, 'w') as f:
            file_writer = csv.DictWriter(f, delimiter=",",
                                         lineterminator="\r", fieldnames=names)

            file_writer.writeheader()


def replace_dict(dict_words: dict, line: str) -> str:
    for old_word, new_word in dict_words.items():
        line = line.replace(str(old_word), str(new_word))

    return line


def read_file(path):
    with codecs.open(path, encoding='utf-8', mode='r') as file:
        for line in file:
            yield line


def read_json_file(path_to_file: str) -> None:
    with open(path_to_file) as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            yield key, value


def create_folder_if_not_exists(loc_name_file):
    if not os.path.exists(loc_name_file):
        os.mkdir(loc_name_file)


def create_file_if_not_exists(loc_name_file):
    if not os.path.exists(loc_name_file):
        with open(loc_name_file, 'w') as f:
            f.write('')


def create_csv_file_if_not_exists(loc_name_file, names=None):
    if names is None:
        names = ["Login", "ID", "Password"]
    # Проверка на существование файла 'reg_user.csv'. Если его не будет - создать.
    if not os.path.exists(loc_name_file):
        with open(loc_name_file, 'w') as f:
            file_writer = csv.DictWriter(f, delimiter=",",
                                         lineterminator="\r", fieldnames=names)

            file_writer.writeheader()


def count_file_in_folder(path, file_name):

    """
    Подсчитывает кол - во файлов в директории.

    :param path:
        Путь до директории, где мы проверяем кол - во файлов.
    :param file_name:
        Строка, которая должна содержаться в имени файла.
    :return:
        Возвращает кол - во таких файлов в директории.
    """

    file_name, count_file = str(file_name), 0
    for i in range(len(os.listdir(path))):
        if file_name in str(os.listdir(path)[i]):
            count_file += 1

    return count_file + 1


def count_lines_in_file(path):

    """
    Считает кол-во строк в файле.

    :param path:
        Путь до файла.
    :return:
        Возвращает кол - во строк.
    """

    with codecs.open(path, 'r', 'utf_8') as f:
        return sum(1 for _ in f)


def attach_file_to_file(path_from, names=None, path_to_save=str(os.getcwd())):

    """
    Объединяет список файлов в один файл.

    :param path_from:
        Путь до файлов.
    :param names:
        Список[] названий этих файлов, включая их тип.
    :param path_to_save:
        Путь, куда надо сохранять результирующий файл.
    :return:
        Ничего не возвращает.
    """

    for i in range(len(names)):
        with codecs.open(path_from + str(names[i]), 'r', 'utf_8') as f:
            print(f.read(), file=codecs.open(path_to_save + '/all_files_result.txt', 'a', 'utf_8'), end='')


def replace_file(path, replace_from, replace_to, bool_list=False):

    """
    Тот же replace только в масштабе файла.

    :param bool_list:
        Проверка, является ли replace_from списком строк или строкой
    :param path:
        Путь до файла.
    :param replace_from:
        Строка, которую нужно удалить в файле.
    :param replace_to:
        Строка, на которую нужно заменить.
    :return:
        Ничего не возвращает.
    """

    with codecs.open(path, 'r', 'utf_8_sig') as f:
        if bool_list:
            str_file = f.read()
            for i in range(len(replace_from)):
                str_file = str_file.replace(replace_from[i], replace_to)

            print(str_file, file=codecs.open(path + '_new.txt', 'w', 'utf_8'), end='')

        else:
            print(f.read().replace(replace_from, replace_to),
                  file=codecs.open(path + '_new.txt', 'w', 'utf_8'), end='')


def del_space(path):

    """
    Удаляет все пустые строки в файле.

    :param path:
        Путь до файла.
    :return:
        Ничего не возвращает.
    """

    with codecs.open(path, 'r', 'utf_8') as f:
        for line in f:
            if line.isspace():
                continue
            else:
                print(line, file=codecs.open(path + 'del_space_RESULT.txt', 'a', 'utf_8'), end='')


def split_file(path):

    """
    Режет один файл на два через строку: _question и _answer

    :param path:
        Путь до файла
    :return:
        Ничего не возвращает.
    """

    with codecs.open(path, 'r', 'utf_8') as f:
        for (offset, line) in enumerate(f):
            if offset % 2 == 0:
                print(line, file=codecs.open(path + '_question', 'a', 'utf_8'), end='')
            else:
                print(line, file=codecs.open(path + '_answer', 'a', 'utf_8'), end='')

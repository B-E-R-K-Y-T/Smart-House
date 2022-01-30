# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

# Апишка для авторизации пользователей

# ----------------------------------------------------------------------------------------------------------------------

import csv

from parse_files import create_csv_file_if_not_exists_async

name_file = 'users.csv'


async def check_exist_user(user_id):
    await create_csv_file_if_not_exists_async(name_file)

    with open(name_file, 'r') as f:
        # Создаем объект DictReader, указываем символ-разделитель ","
        file_reader = csv.DictReader(f, delimiter=",")
        # Считывание данных из CSV файла
        for row in file_reader:
            if str(user_id) == str(row['ID']):
                return True
        else:
            return False


async def sign_up(login, password):
    await create_csv_file_if_not_exists_async(name_file)

    with open(name_file, 'r') as f:
        # Создаем объект DictReader, указываем символ-разделитель ","
        file_reader = csv.DictReader(f, delimiter=",")
        # Считывание данных из CSV файла
        for row in file_reader:
            if login == row['Login'] and password == row['Password']:
                return True
        else:
            return False

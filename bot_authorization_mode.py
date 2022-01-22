# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

# Апишка для авторизации пользователей

# ----------------------------------------------------------------------------------------------------------------------

import csv
import os

name_file = 'users.csv'


async def create_file_if_not_exists(loc_name_file):
    # Проверка на существование файла 'reg_user.csv'. Если его не будет - создать.
    if not os.path.exists(loc_name_file):
        with open(loc_name_file, 'w') as f:
            names = ["Login", "ID", "Password"]
            file_writer = csv.DictWriter(f, delimiter=",",
                                         lineterminator="\r", fieldnames=names)

            file_writer.writeheader()


async def check_exist_user(user_id):
    await create_file_if_not_exists(name_file)

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
    await create_file_if_not_exists(name_file)

    with open(name_file, 'r') as f:
        # Создаем объект DictReader, указываем символ-разделитель ","
        file_reader = csv.DictReader(f, delimiter=",")
        # Считывание данных из CSV файла
        for row in file_reader:
            if login == row['Login'] and password == row['Password']:
                return True
        else:
            return False

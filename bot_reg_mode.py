# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

# Апишка для регистрации пользователей

# ----------------------------------------------------------------------------------------------------------------------

import csv
import os

name_file = 'users.csv'


async def create_file_if_not_exists(loc_name_file):
    # Проверка на существование файла 'reg_user.csv'. Если его не будет - создать.
    if not os.path.exists(loc_name_file):
        with open(loc_name_file, 'w') as f:
            names = ["Login", "Password", "ID"]
            file_writer = csv.DictWriter(f, delimiter=",",
                                         lineterminator="\r", fieldnames=names)

            file_writer.writeheader()


async def get_user(user_id):
    await create_file_if_not_exists(name_file)

    with open(name_file, 'r') as f:
        # Создаем объект DictReader, указываем символ-разделитель ","
        file_reader = csv.DictReader(f, delimiter=",")
        # Считывание данных из CSV файла
        for row in file_reader:
            if user_id == row['ID']:
                return row['Login'], row['ID'], row['Password']
        else:
            return None


async def set_user(login, user_id, password):
    await create_file_if_not_exists(name_file)

    # Запись запроса от бота на сервере в csv - файл
    with open(name_file, 'a') as f:
        names = ["Login", "ID", "Password"]
        file_writer = csv.DictWriter(f, delimiter=",",
                                     lineterminator="\r", fieldnames=names)

        file_writer.writerow(
            {
                names[0]: login,
                names[1]: user_id,
                names[2]: password
            }
        )

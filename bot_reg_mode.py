# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

# Апишка для регистрации пользователей

# ----------------------------------------------------------------------------------------------------------------------

import csv

from parse_files import create_csv_file_if_not_exists_async

name_file = 'users.csv'


async def get_user(user_id):
    await create_csv_file_if_not_exists_async(name_file)

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
    await create_csv_file_if_not_exists_async(name_file)

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

# ======================================================================================================================

# Author: BERKYT

# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------

# api для работы с PostgreSQL

# ----------------------------------------------------------------------------------------------------------------------

import psycopg2
from config_files.config import HOST, USER, PASSWORD, DATABASE

connection = None

try:
    assert isinstance(DATABASE, object)
    connection = psycopg2.connect(
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        host=HOST
    )
except Exception as e:
    print('ERROR[open_db]: {}'.format(e))


def close_db():

    """
    Закрывает БД

    :return:
        Ничего не возвращает.
    """

    try:
        connection.close()
    except Exception as e:
        print('ERROR[close_db]: {}'.format(e))


def inquiry_to_db(inquiry, flag=False):

    """
    Принимает SQL-запрос и выполняет его

    :param inquiry:
        Этот параметр принимает в себя string SQL-запрос.
    :param flag:
        Указывает, надо ли выводить на экран отчет о запросе.
    :return:
        Ничего не возвращает.
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(inquiry)
            connection.commit()
            if flag:
                return cursor.fetchone()
    except Exception as e:
        print('ERROR[inquiry_to_db]: {}'.format(e))

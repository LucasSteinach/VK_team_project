from typing import List

import psycopg2 as psy
import os
from dotenv import load_dotenv, find_dotenv

# по user_id возвращает список id пользователей в избранном (тип строка!)


def select_from_favorite_list(user_id, connection) -> list[str] | str:
    if user_id != '' and user_id is not None:
        select_query = f"SELECT id_person FROM relation_user_person WHERE id_user = {user_id}"
        point = connection.cursor()
        point.execute(select_query)
        records = point.fetchall()
        res = []
        if records is not None:
            for i in range(len(records)):
                res.append(str(records[i][0]))
            return res
        else:
            return "Не удалось выполнить запрос"
    else:
        return "Отсутствует id пользователя"


def sql_connection(db_name, db_user, db_password, db_host, db_port, target_session_attrs, sslmode):
    connection = None
    try:
        connection = psy.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            target_session_attrs=target_session_attrs,
            sslmode=sslmode
        )
        print("Connection to PostgreSQL DB successful")
    except psy.OperationalError as error:
        return f"The error '{error}' occurred"
    return connection


# записывает данные в БД. На вход данные в нужном формате (см. ф-ю prepare_data).
# На вход идут данные, соединение (см. sql_connection), название таблицы (persons или
# users или relation_user_person)
def insert_data(values_data, connection, table_name='relation_user_person'):
    if values_data != '':
        insert_query = f"insert into {table_name} values ({values_data})"
        point = connection.cursor()
        point.execute(insert_query)
        connection.commit()
        return 'successfully inserted'


# готовит данные для загрузки в БД
# на вход идет список, в котором идут данные (неважно, юзер бота или
# предлагаемый человек) в следующем порядке: id (integer, как в ВК), name, city, country, sex
def prepare_data(data_from_bot: list):
    temp_list = list(data_from_bot)
    # для вставки в таблицу строка нужны одинарные кавычки
    temp_list[1] = f"'{temp_list[1]}'"
    input_data = ", ".join(temp_list)
    return input_data


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    # создаем подключение к БД; получаем список избранных аккаунтов

    conn = sql_connection(*os.getenv('sql_auth_data').split(','))
    print(select_from_favorite_list(1, conn))

    # делаю связку аккаунта юзера и предлагаемого человека (2, 2) это строка
    smth = "https://vk.com/2"
    grt = smth.split("/")[-1]
    valu = str(2) + ', ' + grt
    print(valu)

    # создаю запись в таблице (по умолчанию для этой функции таблица избранных)
    insert_data(valu, conn)
    print(select_from_favorite_list(2, conn))

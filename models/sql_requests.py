import psycopg2 as psy
from dotenv import load_dotenv, find_dotenv

# sql_auth_data = (
#     db_name: str,
#     db_user: str,
#     db_password: str,
#     db_host: str,
#     db_port: str,
#     target_session_attrs: str,
#     sslmode: str
# )


def select_from_favorite_list(user_id, connection) -> list[str] | str:
    """
    Функция по user_id возвращает список строк id пользователей в избранном.
    :param user_id: ID пользователя ботом
    :param connection: Созданное в функции sql_connection() подключение к БД
    :return: Список строк id пользователей
    """
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
    """
    Создание нового подключения к БД
    :param db_name: Название БД
    :param db_user: Имя пользователя
    :param db_password: Пароль
    :param db_host: Хост, где располагается БД
    :param db_port: Порт подключения к БД
    :param target_session_attrs: права доступа к БД. в нашем случае "read-write".
    :param sslmode: параметр, определяющий защиту соединения (шифрование) в нашем случае "disabled"
    :return: Созданное подключение "connection" или ошибка подключения
    """
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
        if 'sslmode' in str(error).split(' '):
            return f"Неверно введен аргумент sslmode ('{sslmode}')"
        elif 'target_session_attrs' in str(error).split(' '):
            return f"Неверно введен аргумент target_session_attrs ('{target_session_attrs}')"
        elif 'Unknown' in str(error).split(' '):
            return f"Неверно введен аргумент db_host ('{db_host}')"
        elif 'refused' in str(error).split(' '):
            return f"Неверно введен аргумент db_port ('{db_port}')"
        elif 'authentication' in str(error).split(' '):
            return f"Ошибка аутентификации (неверный логин или пароль)"
        elif f'"{db_name}"' in str(error).split(' '):
            return f"Базы данных '{db_name}' не существует"

        return str(error)
    return connection


def create_tables(connection):
    query = f"""CREATE TABLE IF NOT EXISTS users
        (
            id INTEGER NOT NULL,
            name CHARACTER VARYING(80) COLLATE pg_catalog."default" NOT NULL,
            city INTEGER,
            country INTEGER,
            sex INTEGER,
            CONSTRAINT users_pkey PRIMARY KEY (id)
        );
        
        
        CREATE TABLE IF NOT EXISTS persons
        (
            id INTEGER NOT NULL,
            name CHARACTER VARYING(80) COLLATE pg_catalog."default" NOT NULL,
            city INTEGER,
            country INTEGER,
            sex INTEGER,
            CONSTRAINT persons_pkey PRIMARY KEY (id)
        );
        
        
        CREATE TABLE IF NOT EXISTS relation_user_person
        (
            id_user INTEGER NOT NULL,
            id_person INTEGER NOT NULL,
            CONSTRAINT const_person FOREIGN KEY (id_person)
                REFERENCES public.persons (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID,
            CONSTRAINT const_user FOREIGN KEY (id_user)
                REFERENCES public.users (id) MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID
        );
    """
    point = connection.cursor()
    point.execute(query)
    connection.commit()
    return 'successfully created'


def insert_data(values_data, connection, table_name='relation_user_person'):
    """
    Функция записывает данные в БД. На вход принимает данные в нужном формате
    (см. функцию prepare_data).
    На вход идут данные, соединение (см. sql_connection), название таблицы (persons или
    users или relation_user_person)
    :param values_data: Данные для записи
    :param connection: Созданное подключение к БД
    :param table_name: Название таблицы
    :return: Сообщение об успешном добавлении данных в целевую таблицу
    """
    if values_data != '':
        insert_query = f"insert into {table_name} values ({values_data})"
        point = connection.cursor()
        point.execute(insert_query)
        connection.commit()
        return 'successfully inserted'


def prepare_data(data_from_bot: list):
    """
    Функция подготовки данных к загрузке в БД. На вход принимает данные о пользователе
    (бота или найденного человека) в следующем порядке:
    id (int, как в ВК), name, city, country, sex
    :param data_from_bot: Данные, полученные от бота в виде списка
    :type data_from_bot: list
    :return: Подготовленные для вставки в БД данные (input_data)
    """
    temp_list = [str(i) for i in data_from_bot]
    # для вставки в таблицу строка нужны одинарные кавычки
    temp_list[1] = f"'{temp_list[1]}'"
    input_data = ", ".join(temp_list)
    return input_data


def select_from_table(connection, table_name) -> list:
    """
    Функция поиска id в таблицах 'persons' или 'users'
    :param connection: Созданное подключение к БД
    :param table_name: Название таблицы, из которой производится выборка
    :return: Список id пользователей из 'persons' или 'users'
    """
    if table_name == 'persons' or table_name == 'users':
        select_query = f"SELECT id FROM {table_name}"
        point = connection.cursor()
        point.execute(select_query)
        records = point.fetchall()
        res = []
        if records is not None:
            for i in range(len(records)):
                res.append(int(records[i][0]))
        return res


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    # создаем подключение к БД; получаем список избранных аккаунтов
    # conn = sql_connection(*os.getenv('sql_auth_data').split(','))
    # print(select_from_favorite_list(1, conn))

    # делаю связку аккаунта юзера и предлагаемого человека (2, 2) это строка
    # smth = "https://vk.com/2"
    # grt = smth.split("/")[-1]
    # valu = str(2) + ', ' + grt
    # print(valu)

    # создаю запись в таблице (по умолчанию для этой функции таблица избранных)
    # insert_data(valu, conn)
    # print(select_from_favorite_list(2, conn))

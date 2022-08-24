from models.sql_requests import insert_data, prepare_data


def check_user_presens(user_id, name, city, country, sex, user_storage):
    if user_id not in user_storage:
        insert_data(prepare_data([user_id, name, city, country, sex]),connection, table_name='users')

def check_owner_presens(user_id, name, city, country, sex, profile_storage):
    if user_id not in profile_storage:
        insert_data(prepare_data([user_id, name, city, country, sex]),connection, table_name='persons')
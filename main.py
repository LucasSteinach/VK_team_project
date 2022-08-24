from CLASS_VK.vk_classes import VK, VK_bot
import os
from dotenv import load_dotenv, find_dotenv
from time import sleep
from datetime import datetime
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import random

from models.processing_responses import determine_gender
from models.sql_requests import select_from_favorite_list, \
    sql_connection, insert_data, prepare_data, select_from_table, create_tables
from models.send_fun import write_msg, write_msg_attachment
from models.func_for_BD import check_user_presens, check_owner_presens

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    try:
        vk = vk_api.VkApi(token=os.getenv('KEY_VKinderPy'))
        longpoll = VkLongPoll(vk)
    except:
        print(' Ошибка доступа к API VK!:\n1.проверьте соединение.\n2.проверьте ключ доступа.')

    connection = sql_connection(*os.getenv('sql_auth_data').split(','))
    create_tables(connection)
    favorites_profiles = []
    user_storage = select_from_table(connection, 'users')
    profile_storage = select_from_table(connection, 'persons')



    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                sleep(0.33)

                request = event.text.lower()
                VK_bot(os.getenv('KEY_VKinderPy'),
                       event.user_id).comand_request(request,
                                                     profile_storage,
                                                     favorites_profiles,
                                                     connection, user_storage)

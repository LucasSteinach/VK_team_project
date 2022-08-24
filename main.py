from CLASS_VK.vk_classes import VK, VK_bot
import os
from dotenv import load_dotenv, find_dotenv

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
    connection = sql_connection(*os.getenv('sql_auth_data').split(','))
    create_tables(connection)
    favorites_profiles = []
    user_storage = select_from_table(connection, 'users')
    profile_storage = select_from_table(connection, 'persons')

    vk = vk_api.VkApi(token=os.getenv('KEY_VKinderPy'))
    longpoll = VkLongPoll(vk)

    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:

                # if len(favorites_profiles) == 0:
                #     favorites_profiles = select_from_favorite_list(event.user_id, connection)
                #     favorites_profiles = ["https://vk.com/id" + str(i) for i in favorites_profiles]

                request = event.text.lower()
                VK_bot(os.getenv('KEY_VKinderPy'), event.user_id).comand_request(request, profile_storage,
                                                                                 favorites_profiles, connection)
                # user = VK(os.getenv('VK_MYTOKEN'))
                # info_bot_user = user.get_users_info(event.user_id)
                # name_bot_user = info_bot_user['response'][0]['first_name']
                #
                # if 'city' in info_bot_user['response'][0].keys(): #убрать эту логику
                #     city = info_bot_user['response'][0]['city']['id']
                # else:
                #     city = 0
                # if 'country' in info_bot_user['response'][0].keys():
                #     country = info_bot_user['response'][0]['country']['id']
                # else:
                #     country = 0
                #
                # sex = determine_gender(info_bot_user)
                #
                # if event.user_id not in user_storage: #убрано под check_users_presens
                #     insert_data(prepare_data([event.user_id,
                #                               name_bot_user,
                #                               city, country,
                #                               info_bot_user['response'][0]['sex']]),
                #                 connection,
                #                 table_name='users')
                #
                # if 'bdate' in info_bot_user['response'][0].keys() and \
                #         len(info_bot_user['response'][0]['bdate']) > 7:
                #     age_bot_user = int(info_bot_user['response'][0]['bdate'][-4:])
                #
                #     age_to = (int(datetime.now().year) - age_bot_user) + 2
                #     age_from = (int(datetime.now().year) - age_bot_user) - 7
                # else:
                #     age_to = None
                #     age_from = None
                #
                # owners = VK(os.getenv('VK_MYTOKEN'))
                #
                # id_list = owners.get_info_owner_usersearch(city, sex, age_to, age_from)
                # owner_id = random.choice(id_list)
                #
                # info_owner = user.get_users_info(owner_id)
                #
                # if owner_id not in profile_storage:
                #     name_owner = info_owner['response'][0]['first_name']
                #     if 'city' in info_owner['response'][0].keys():
                #         city_owner = info_bot_user['response'][0]['city']['id']
                #     else:
                #         city_owner = 0
                #     if 'country' in info_owner['response'][0].keys():
                #         country_owner = info_owner['response'][0]['country']['id']
                #     else:
                #         country_owner = 0
                #     sex_owner = info_owner['response'][0]['sex']
                #     insert_data(prepare_data([owner_id, name_owner, city_owner, country_owner, sex_owner]),
                #                 connection,
                #                 table_name='persons')
                #
                # profile_storage.append(int(owner_id))
                # profile_storage.append(f"https://vk.com/{info_owner['response'][0]['domain']}")
                #
                # keyboards = VkKeyboard(one_time=False)
                # begin = VkKeyboard(one_time=True)
                #
                # begin.add_button('начать', VkKeyboardColor.PRIMARY)
                #
                # if request == "привет":
                #
                #     write_msg(event.user_id, f"Привет!\n{name_bot_user}",
                #               vk_authoriz=vk,
                #               keyboard=begin.get_keyboard())
                #
                # elif request == "начать":
                #     keyboards.add_button('продолжить', VkKeyboardColor.POSITIVE)
                #     keyboards.add_line()
                #     keyboards.add_button('в избранное', VkKeyboardColor.PRIMARY)
                #     keyboards.add_button('избранное', VkKeyboardColor.SECONDARY)
                #
                #     write_msg(event.user_id, f"""нажмите "продолжить" для продолжения""",
                #               vk_authoriz=vk,
                #               keyboard=keyboards.get_keyboard())
                #
                # elif request == 'продолжить':
                #
                #     if owner_id not in profile_storage:
                #
                #         name_owner = info_owner['response'][0]['first_name']
                #         city_owner = info_owner['response'][0]['city']['id']
                #
                #         if city_owner is None:
                #             city_owner = 0
                #         country_owner = info_owner['response'][0]['country']['id']
                #
                #         if country_owner is None:
                #             country_owner = 0
                #         sex_owner = info_owner['response'][0]['sex']
                #         insert_data(prepare_data([owner_id, name_owner, city_owner, country_owner, sex_owner]),
                #                     connection,
                #                     table_name='persons')
                #
                #     attachments = user.get_photo(owner_id)
                #
                #     #сюда складываем ссылки на все просмотренные профили
                #     profile_storage.append(int(owner_id))
                #     profile_storage.append(f"https://vk.com/{info_owner['response'][0]['domain']}")
                #
                #     write_msg_attachment(event.user_id,
                #                          f"Вот,что мы подобрали для вас!,\n"
                #                          f"https://vk.com/{info_owner['response'][0]['domain']}\n"
                #                          f"{info_owner['response'][0]['first_name']} "
                #                          f"{info_owner['response'][0]['last_name']}",
                #                          vk_authoriz=vk, attachments=attachments)
                #
                # elif request == 'в избранное':
                #     if len(profile_storage) > 0:
                #         favorites_profiles.append(profile_storage[-1])
                #
                #         rel_user_person = str(event.user_id) + ', ' + str(owner_id)
                #         insert_data(rel_user_person, connection)
                #     else:
                #         pass
                #
                # elif request == 'избранное':
                #     if len(favorites_profiles) > 0:
                #         for link in set(favorites_profiles):
                #             write_msg(event.user_id, f"{link}", vk_authoriz=vk)
                #     else:
                #         write_msg(event.user_id, '''у вас пока нет избранных контактов\n'''
                #                                  '''чтобы добавить нажмите \n"в избранное"''',
                #                   vk_authoriz=vk)
                #
                # elif request == "пока":
                #     write_msg(event.user_id,
                #               "До свидания, приходите снова",
                #               vk_authoriz=vk)
                # else:
                #     write_msg(event.user_id,
                #               "Непонятно( лучше нажмите одну из кнопок ниже",
                #               vk_authoriz=vk)

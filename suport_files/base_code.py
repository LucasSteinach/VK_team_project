import os
from dotenv import load_dotenv, find_dotenv

from requests_info_vk_fun import get_info_owner_usersearch, get_info_owner_userget, get_photo, \
    get_info_bot_user, determine_gender
from sql_requests import select_from_favorite_list, sql_connection, insert_data, prepare_data
from pprint import pprint
from datetime import datetime
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
from send_fun import write_msg, write_msg_attachment
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random

# см. личное сообщение про sql_auth_data
connection = sql_connection(*sql_auth_data)
favorites_profiles = []
profile_storage = []

load_dotenv(find_dotenv())
vk = vk_api.VkApi(token=os.getenv('KEY_VKinderPy'))
longpoll = VkLongPoll(vk)

upload = VkUpload(vk)

if __name__ == '__main__':

    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                usr_id = event.user_id
                request = event.text.lower()
                print(event.user_id)
                favorites_profiles = select_from_favorite_list(event.user_id, connection)


                info_bot_user = get_info_bot_user(os.getenv('VK_MYTOKEN'), event.user_id)
                # Парметры поиска:
                city = info_bot_user['response'][0]['city']['id']
                sex = determine_gender(info_bot_user)

                name_bot_user = info_bot_user['response'][0]['first_name']

                #у пользоватля бота должен быть открыт год рождения
                if 'bdate' in info_bot_user['response'][0].keys() and \
                        len(info_bot_user['response'][0]['bdate']) > 7:
                    age_bot_user = int(info_bot_user['response'][0]['bdate'][-4:])

                    age_to = (int(datetime.now().year) - age_bot_user) + 5
                    age_from = (int(datetime.now().year) - age_bot_user) - 15
                else:
                    age_to = None
                    age_from = None

                id_list = get_info_owner_usersearch(os.getenv('VK_MYTOKEN'), city, sex, age_to, age_from)
                owner_id = random.choice(id_list)

                info_owner = get_info_owner_userget(os.getenv('VK_MYTOKEN'), owner_id)
                keyboards = VkKeyboard(one_time=False)
                begin = VkKeyboard(one_time=True)

                begin.add_button('начать', VkKeyboardColor.PRIMARY)

                if request == "привет":

                    write_msg(event.user_id, f"Привет!\n{name_bot_user}",
                              vk_authoriz=vk,
                              keyboard=begin.get_keyboard())

                elif request == "начать":
                    keyboards.add_button('продолжить', VkKeyboardColor.POSITIVE)
                    keyboards.add_line()
                    keyboards.add_button('в избранное', VkKeyboardColor.PRIMARY)
                    keyboards.add_button('избранное', VkKeyboardColor.SECONDARY)

                    write_msg(event.user_id, f"""нажмите "продолжить" для продолжения""",
                              vk_authoriz=vk,
                              keyboard=keyboards.get_keyboard())

                elif request == 'продолжить':

                    info_owner = get_info_owner_userget(os.getenv('VK_MYTOKEN'), owner_id)
                    attachments = get_photo(os.getenv('VK_MYTOKEN'), owner_id)

                    #сюда складываем ссылки на все просмотренные профили
                    profile_storage.append(f" https://vk.com/{info_owner['response'][0]['domain']}")

                    write_msg_attachment(event.user_id,
                                         f"Вот,что мы подобрали для вас!,\n"
                                         f"https://vk.com/{info_owner['response'][0]['domain']}\n"
                                         f"{info_owner['response'][0]['first_name']} "
                                         f"{info_owner['response'][0]['last_name']}",
                                         vk_authoriz=vk, attachments=attachments)

                elif request == 'в избранное':
                    if len(profile_storage) > 0:
                        favorites_profiles.append(profile_storage[-1])
                        rel_user_person = event.user_id + ', ' + str(owner_id)
                        insert_data(rel_user_person, connection)
                    else:
                        pass

                elif request == 'избранное':
                    if len(favorites_profiles) > 0:
                        for link in set(favorites_profiles):
                            write_msg(event.user_id, f"{link}", vk_authoriz=vk)
                    else:
                        write_msg(event.user_id, "у вас пока нет избранных контактов",
                                  vk_authoriz=vk)

                elif request == "пока":
                    write_msg(event.user_id,
                              "До свидания, приходите снова",
                              vk_authoriz=vk)
                else:
                    write_msg(event.user_id,
                              "Непонятно( лучше нажмите одну из кнопок ниже",
                              vk_authoriz=vk)

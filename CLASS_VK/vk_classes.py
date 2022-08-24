import time
from pprint import pprint
import os
import requests
from dotenv import load_dotenv, find_dotenv

from CLASS_work_list.class_ListWork import ListWork
from models.processing_responses import determine_gender
import random
from datetime import datetime
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import vk_api

from models.send_fun import write_msg, write_msg_attachment
from models.sql_requests import select_from_favorite_list, insert_data
from models.func_for_BD import check_owner_presens, check_user_presens

class VK:
    """
            Класс VK используется для получения информации о пользователе.

            Attributes
            ----------
            :param token: Ключ доступа пользователя ВК
            :type token: str

            :param version Актуальная версия VK API, на ткущий момент - 5.131
            :type version: str

            :param params Параметры для запроса к API Вконтакте
            :type params: dict

            Methods
            -------
            get_users_info()
                Формирует запрос на получение информации о пользователе.
                Возвращает информацию о пользователе в формате json.

            get_info_owner_usersearch()
                Поиск информации о пользователе для отправки сообщения

            get_photo()
                Поиск популярных фото и формирование списка фотографий.
            """

    def __init__(self, access_token, version='5.131'):
        self.token = access_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.path = 'https://api.vk.com/method/'

    def get_users_info(self, user_id):
        """
            Используем этот метод с разными id(event.user_id и owner_id) пользователей -
            для пользователя бота и найденных пользователей

            :param user_id ID пользователя
            :type user_id: int

            Метод возвращает информацию о пользователе (день рождения, пол, город, короткий
            адрес страницы, страну - в формате json)
        """
        method = 'users.get'
        url = self.path + method
        params = {'user_ids': user_id, 'fields': 'bdate,sex,city,domain,country',
                  'v': '5.131'}

        res = requests.get(url, params={**self.params, **params})
        return res.json()

    def get_info_owner_usersearch(self, city, sex=1, age_to=50, age_from=19, count=1000):
        """
            Поиск информации о пользователе для отправки сообщения

            :param city Город найденного пользователя
            :type city: str

            :param sex Пол пользователя. 1 - женский, 2 - мужской, 0 - пол не указан
            :type sex: int

            :param age_to Возраст до которого ищется совпадение
            :type age_to: int

            :param age_from Возраст от которого ищутся совпадения
            :type age_from: int

            :param count Количество аккаунтов для поиска. Максимально 1000 в одном запросе
            :type count: int

            Метод возвращает список id пользователей
        """
        method = 'users.search'
        url = self.path + method
        params = {'v': '5.131',
                  'fields': 'bdate,sex,city,domain,country',
                  'city': city,
                  'count': count,
                  'sex': sex,
                  'age_to': age_to,
                  'age_from': age_from
                  }
        res = requests.get(url, params={**self.params, **params})
        # pprint(res.json()['response']['items'])
        if 'response' in res.json():
            inf_user = res.json()['response']['items']

            list_id = [users_id['id'] for users_id in inf_user]
            # pprint(res.json())
            return list_id


    def get_photo(self, owner_id, count=15):
        """
             Поиск популярных фото и формирование списка фотографий.

             :param owner_id ID пользователя бота.
             :type owner_id: int

             :param count Количество фотографий.
             :type count: int

             Метод возвращает список фотографий в формате медиавложений <type><ownerid><media_id> для
             параметра attachment в методе messages.send (каждый элемент списка - type str),
             а если фотографии пользователя найти не удалось - возвращает фото сообщества.
         """
        dict_photo = {}
        method = 'photos.get'
        url = self.path + method

        params = {'album_id': 'profile',
                  'extended': 1,
                  'rev': 0,
                  'owner_id': owner_id,
                  'v': '5.131', 'count': count}
        res = requests.get(url, params={**self.params, **params})

        time.sleep(0.333)

        if 'response' in res.json().keys() and \
                len(res.json()['response']['items']) > 0 and \
                'error' not in res.json().keys():

            for photos in res.json()['response']['items']:
                dict_photo[photos['likes']['count'], photos['id']] = f"photo{photos['owner_id']}_{photos['id']}"

            list_send_photo = []
            if len(dict_photo) >= 3:
                list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 1]])
                list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 2]])
                list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 3]])

            elif 1 < len(dict_photo) <= 2:
                list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 1]])
                list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 2]])

            elif 0 < len(dict_photo) <= 1:
                list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 1]])

            print(','.join(list_send_photo))
            return ','.join(list_send_photo)

        elif 'response' in res.json().keys() and \
                len(res.json()['response']['items']) == 0:
            print(' ЭТО ФОТО СООБЩЕСТВА photo-214911415_457239017')  # если фото с аватаров нет
            return 'photo-214911415_457239017'

        elif 'error' in res.json().keys():  # если страница закрта для просмотра фото с аватара
            return 'photo-214911415_457239589'


        elif 'error' in res.json().keys():  # если страница закрта для просмотра фото с аватара
            return 'photo-214911415_457239589'

class VK_bot:

    def __init__(self, token_key_group_vk, event_user_id):
        self.token = token_key_group_vk
        self.comand = ['привет', 'начать', 'продолжить', 'в избранное', 'избранное', 'пока']
        self.user_id = event_user_id



    def comand_request(self, request, list_1, list_2, connection, user_storage, profile_storage ):

        inf = VK(os.getenv('VK_MYTOKEN'))


        name = inf.get_users_info(self.user_id)['response'][0]['first_name']
        city = inf.get_users_info(self.user_id)['response'][0]['city']['id']
        country = inf.get_users_info(self.user_id)['response'][0]['country']['id']
        sex = determine_gender(inf.get_users_info(self.user_id))
        sex_user = inf.get_users_info(self.user_id)['response'][0]['sex']

        check_user_presens(self.user_id, name, city, country, sex_user, user_storage)


        # функции БД
        if len(list_2) == 0:
            list_2 = select_from_favorite_list(self.user_id, connection)
            list_2 = ["https://vk.com/id" + str(i) for i in list_2]


        if 'bdate' in inf.get_users_info(self.user_id)['response'][0].keys() and \
                len(inf.get_users_info(self.user_id)['response'][0]['bdate']) > 7:

            age_bot_user = int(inf.get_users_info(self.user_id)['response'][0]['bdate'][-4:])

            age_to = (int(datetime.now().year) - age_bot_user) + 5
            age_from = (int(datetime.now().year) - age_bot_user) - 5

        else:
            age_to = None
            age_from = None

        id_list = inf.get_info_owner_usersearch(city, sex, age_to, age_from)


        keyboards = VkKeyboard(one_time=False)
        begin = VkKeyboard(one_time=True)
        begin.add_button('Начать', VkKeyboardColor.PRIMARY)

        if request == self.comand[0]:
            print('Проверка')
            write_msg(self.user_id, f"\nПривет!\n{name}",
                      vk_authoriz=vk_api.VkApi(token=self.token), keyboard=begin.get_keyboard())

        elif request == self.comand[1]:

            keyboards.add_button('Продолжить', VkKeyboardColor.POSITIVE)
            keyboards.add_line()
            keyboards.add_button('В избранное', VkKeyboardColor.PRIMARY)
            keyboards.add_button('Избранное', VkKeyboardColor.SECONDARY)

            write_msg(self.user_id, f"""нажмите "продолжить" для для получения первого результата""",
                      vk_authoriz=vk_api.VkApi(token=self.token),
                      keyboard=keyboards.get_keyboard())
        owner_id = random.choice(id_list)
        if request == self.comand[2]:


            print(inf.get_users_info(owner_id))
            attachments = inf.get_photo(owner_id)

            write_msg_attachment(self.user_id, f"Вот,что мы подобрали для вас!,\n"
                                         f"https://vk.com/{inf.get_users_info(owner_id)['response'][0]['domain']}\n"
                                         f"{inf.get_users_info(owner_id)['response'][0]['first_name']} "
                                         f"{inf.get_users_info(owner_id)['response'][0]['last_name']}",
                                         vk_authoriz=vk_api.VkApi(token=self.token), attachments=attachments)
            list_1.append(int(owner_id))
            list_1.append(f"https://vk.com/{inf.get_users_info(owner_id)['response'][0]['domain']}")

            name = inf.get_users_info(owner_id)['response'][0]['first_name']
            city = inf.get_users_info(owner_id)['response'][0]['city']['id']
            country = inf.get_users_info(owner_id)['response'][0]['country']['id']
            sex_owner = inf.get_users_info(self.user_id)['response'][0]['sex']

            check_owner_presens(self.user_id, name, city, country, sex_owner, profile_storage)

            return f"https://vk.com/{inf.get_users_info(owner_id)['response'][0]['domain']}"

        elif request == self.comand[3]:
            ListWork(list_1, list_2).add_favorites()
            rel_user_person = str(self.user_id) + ', ' + str(owner_id)
            insert_data(rel_user_person, connection)



        elif request == self.comand[4]:
            favorites = ListWork(list_1, list_2).get_favorites()

            if isinstance(favorites, set):
                for link in favorites:
                    write_msg(self.user_id, f"{link}", vk_authoriz=vk_api.VkApi(token=self.token))
            else:
                write_msg(self.user_id, f"У вас пока нет избранных контактов",
                          vk_authoriz=vk_api.VkApi(token=self.token))

        elif request == self.comand[5]:
            write_msg(self.user_id, f"До свидания!, приходите снова)",
                      vk_authoriz=vk_api.VkApi(token=self.token))
        else:
            write_msg(self.user_id, 'Я не понимаю(\nпопробуйте нажать одну из копок:\n"Продолжить", '
                                    '"В избранное"\n или "Избоанное"',
                      vk_authoriz=vk_api.VkApi(token=self.token))



if __name__ == '__main__':
    load_dotenv(find_dotenv())
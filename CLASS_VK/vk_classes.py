import time
from pprint import pprint
import os
import requests
from dotenv import load_dotenv, find_dotenv

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

    def get_users_info(self, user_id):
        """
            Используем этот метод с разными id(event.user_id и owner_id) пользователей -
            для пользователя бота и найденных пользователей

            :param user_id ID пользователя
            :type user_id: int

            Метод возвращает информацию о пользователе (день рождения, пол, город, короткий
            адрес страницы, страну - в формате json)
        """
        url = 'https://api.vk.com/method/users.get'
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
        URl = 'https://api.vk.com/method/users.search'
        params = {'v': '5.131',
                  'fields': 'bdate,sex,city,domain',
                  'city': city,
                  'count': count,
                  'sex': sex,
                  'age_to': age_to,
                  'age_from': age_from
                  }
        res = requests.get(URl, params={**self.params, **params})
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
        URl = 'https://api.vk.com/method/photos.get'

        params = {'album_id': 'profile',
                  'extended': 1,
                  'rev': 0,
                  'owner_id': owner_id,
                  'v': '5.131', 'count': count}
        res = requests.get(URl, params={**self.params, **params})
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


if __name__ == '__main__':
    load_dotenv(find_dotenv())

    user333 = VK(os.getenv('VK_MYTOKEN'))
    inf = user333.get_users_info(13708102)
    pprint(inf)
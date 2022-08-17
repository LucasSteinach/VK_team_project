import time
from pprint import pprint
import os
import requests
from dotenv import load_dotenv, find_dotenv

class VK:

    def __init__(self, access_token, version='5.131'):

        self.token = access_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_users_info(self, user_id):
        #используем этот метод с разными id(event.user_id и owner_id) пользователей
        # для пользователя бота и найденных пользователей
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': user_id, 'fields': 'bdate,sex,city,domain',
                  'v': '5.131'}

        res = requests.get(url, params={**self.params, **params})
        return res.json()


    def get_info_owner_usersearch(self, city, sex=1, age_to=50, age_from=19, count=1000):
        # поиск информации о пользователе для отправки сообщения
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
        #находит фото с аваторов и формириует список трех популярных фото
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






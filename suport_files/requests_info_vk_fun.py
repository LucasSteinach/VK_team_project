import time
from pprint import pprint

import requests
from dotenv import load_dotenv, find_dotenv


def get_photo(access_token, owner_id, count=5):
    # поиск трех популярных фото и формирования списка для attachment
    dict_photo = {}
    URl = 'https://api.vk.com/method/photos.get'

    params = {'album_id': 'profile', 'access_token': access_token,
              'extended': 1, 'rev': 0, 'owner_id': owner_id, 'v': '5.131', 'count': count}
    res = requests.get(URl, params=params)
    time.sleep(0.333)

    if 'response' in res.json().keys() and\
            len(res.json()['response']['items']) > 0 and\
            'error' not in res.json().keys():

        for photos in res.json()['response']['items']:
            dict_photo[photos['likes']['count'], photos['id']] = f"photo{photos['owner_id']}_{photos['id']}"

        list_send_photo = []
        if len(dict_photo) >= 3:
            list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 1]])
            list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 2]])
            list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 3]])

        if 1 < len(dict_photo) <= 2:
            list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 1]])
            list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 2]])

        if 0 < len(dict_photo) <= 1:
            list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 1]])

        print(','.join(list_send_photo))
        return ','.join(list_send_photo)

    if 'response' in res.json().keys() and \
            len(res.json()['response']['items']) == 0:

        print(' ЭТО ФОТО СООБЩЕСТВА photo-214911415_457239017') # если фото с аватаров нет
        return 'photo-214911415_457239017'

    if 'error' in res.json().keys(): #если страница закрта для просмотра фото с аватара
        return 'photo-214911415_457239589'


def get_info_owner_usersearch(access_token, city, sex=1, age_to=50, age_from=19, count=1000):
    # поиск информации о пользователе для отправки сообщения
    URl = 'https://api.vk.com/method/users.search'
    params = {'access_token': access_token,
              'v': '5.131',
              'fields': 'bdate,sex,city,domain',
              'city': city,
              'count': count,
              'sex': sex,
              'age_to': age_to,
              'age_from': age_from
              }
    res = requests.get(URl, params=params, )
    # pprint(res.json()['response']['items'])
    if 'response' in res.json():
        inf_user = res.json()['response']['items']

        list_id = [users_id['id'] for users_id in inf_user]
        pprint(res.json())
        return list_id

def get_info_owner_userget(access_token, owner_id):
    # поиск информации о пользователе для отправки сообщения
    URl = 'https://api.vk.com/method/users.get'
    params = {'access_token': access_token, 'fields': 'bdate,sex,city,domain',
              'user_ids': owner_id, 'v': '5.131'}
    res = requests.get(URl, params=params)

    return res.json()




def get_info_bot_user(access_token, event_user_id):
    # информация о пользователе, которому отправляется сообщение
    URl = 'https://api.vk.com/method/users.get'
    params = {'access_token': access_token, 'fields': 'bdate,sex,city,domain',
              'user_ids': event_user_id, 'v': '5.131'}
    res = requests.get(URl, params=params,)
    print(res.status_code)
    # pprint(res.json())
    return res.json()


def determine_gender(response_json):
    # определяет противоположный пол для ответов полученных методом users.get

    if response_json['response'][0]['sex'] == 1:
        return 2
    if response_json['response'][0]['sex'] == 2:
        return 1
    else:
        return 0




if __name__ == '__main__':
    load_dotenv(find_dotenv())






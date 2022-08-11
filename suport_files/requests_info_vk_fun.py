import time
from pprint import pprint
from random import randrange

import os
import requests
from dotenv import load_dotenv, find_dotenv


def get_photo(access_token, owner_id, count=15):
    # поиск трех популярных фото и формирования списка для attachment
    dict_photo = {}
    URl = 'https://api.vk.com/method/photos.get'

    params = {'album_id': 'profile', 'access_token': access_token,
              'extended': 1, 'rev': 0, 'owner_id': owner_id, 'v': '5.131', 'count': count}
    res = requests.get(URl, params=params)
    time.sleep(0.5)
    pprint(res.json())


    if 'response' in res.json().keys() and\
            len(res.json()['response']['items']) > 0 and\
            'error' not in res.json().keys():

        for photos in res.json()['response']['items']:
            dict_photo[photos['likes']['count'], photos['id']] = f"photo{photos['owner_id']}_{photos['id']}"
            # print(f"{photos['likes']['count']} - {photos['sizes'][2]['url']}")

        pprint(dict_photo)

        list_send_photo = []
        if len(sorted(dict_photo)) >= 3:
            list_send_photo.append(dict_photo[sorted(dict_photo)[len(sorted(dict_photo)) - 1]])
            list_send_photo.append(dict_photo[sorted(dict_photo)[len(sorted(dict_photo)) - 2]])
            list_send_photo.append(dict_photo[sorted(dict_photo)[len(sorted(dict_photo)) - 3]])

        if 1 < len(sorted(dict_photo)) <= 2:
            list_send_photo.append(dict_photo[sorted(dict_photo)[len(sorted(dict_photo)) - 1]])
            list_send_photo.append(dict_photo[sorted(dict_photo)[len(sorted(dict_photo)) - 2]])

        if 0 < len(sorted(dict_photo)) <= 1:
            list_send_photo.append(dict_photo[sorted(dict_photo)[len(sorted(dict_photo)) - 1]])

        # print(list_send_photo)
        print(','.join(list_send_photo))
        return ','.join(list_send_photo)

    if 'response' in res.json().keys() and \
            len(res.json()['response']['items']) == 0:

        print('ФОТО СООБЩЕСТВА photo-214911415_457239017')
        return 'photo-214911415_457239017'





def get_info_owner(access_token):
    # поиск информации о пользователе для отправки сообщения
    URl = 'https://api.vk.com/method/users.get'
    params = {'access_token': access_token, 'fields': 'bdate,sex,city,domain',
              'user_ids': randrange(10**7), 'v': '5.131'}
    res = requests.get(URl, params=params, )

    if 'response' in res.json().keys() and\
            'deactivated' not in res.json()['response'][0].keys()\
            and res.json()['response'][0]['is_closed'] is False:

        get_photo(os.getenv('VK_MYTOKEN'), res.json()['response'][0]['id'])
        pprint(res.json())


        return res.json()
    else:
        return get_info_owner(access_token)


def get_info_bot_user(access_token, event_user_id):
    # информация о пользователе, которому отправляется сообщение
    URl = 'https://api.vk.com/method/users.get'
    params = {'access_token': access_token, 'fields': 'bdate,sex,city,domain',
              'user_ids': event_user_id, 'v': '5.131'}
    res = requests.get(URl, params=params,)
    pprint(res.json())

    return res.json()

def compare_parametrs(access_token, info_bot_user):
    # сравнивет аналогичные параметры и находит пользователя при совпадении
    info_owner = get_info_owner(access_token)

    if info_owner['response'][0]['sex'] != info_bot_user['response'][0]['sex']:

        return info_owner
    else:
        return compare_parametrs(access_token, info_bot_user)






if __name__ == '__main__':
    load_dotenv(find_dotenv())
    # get_photo(os.getenv('VK_MYTOKEN'), 81658)
    info_ow = get_info_owner(os.getenv('VK_MYTOKEN'))
    # print(info_ow)
    # info_bot_user = get_info_bot_user(os.getenv('VK_MYTOKEN'), 9668538)
    # print(f"{info_bot_user['response'][0]['city']['title']}\n{info_bot_user['response'][0]['sex']}")

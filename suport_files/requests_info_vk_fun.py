
from pprint import pprint
from random import randrange

import os
import requests
from dotenv import load_dotenv, find_dotenv


def get_photo(access_token, owner_id, count=100):

    dict_photo = {}
    URl = 'https://api.vk.com/method/photos.get'
    params = {'album_id': 'profile', 'access_token': access_token, 'extended': 1, 'rev': 0, 'owner_id': owner_id, 'v': '5.131', 'count': count}
    res = requests.get(URl, params=params)
    # pprint(res.json())


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

        print(list_send_photo)
        print(','.join(list_send_photo))
        return ','.join(list_send_photo)



def get_info_owner(access_token, id_user='13708102'):

    URl = 'https://api.vk.com/method/users.get'
    params = {'access_token': access_token, 'fields': 'bdate,sex,city,domain',
              'user_ids': randrange(10 ** 7), 'v': '5.131'}
    res = requests.get(URl, params=params, )
    dict_res = res.json()
    if 'deactivated' not in dict_res['response'][0].keys():
        get_photo(os.getenv('VK_MYTOKEN'), dict_res['response'][0]['id'])
        pprint(dict_res)

        return res.json()
    else:
        get_info_owner(access_token)

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    get_info_owner(os.getenv('VK_MYTOKEN'))
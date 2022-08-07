import os
from pprint import pprint
from random import randrange
import urllib.request

import requests

from dotenv import load_dotenv, find_dotenv


class VK:

   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def users_info(self):
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params})
       return response.json()

user_id = '13708102'
load_dotenv(find_dotenv())

vk = VK(os.getenv('VK_MYTOKEN'), user_id)



def get_photo(access_token, count=10):
    dict_photo = {}
    URl = 'https://api.vk.com/method/photos.get'
    params = {'album_id': 'profile', 'access_token': access_token, 'extended': 1, 'rev': 0, 'owner_id': randrange(10 ** 7), 'v': '5.131', 'count': count}
    res = requests.get(URl, params=params)
    pprint(res.json())
    # pprint(f"Лайки {res.json()['response']['items'][0]['likes']['count']},{res.json()['response']['items'][0]['sizes'][2]['url']}")
    if len(res.json()['response']['items']) > 0:
        for photos in res.json()['response']['items']:
            dict_photo[photos['likes']['count'], photos['id']] = photos['sizes'][2]['url']
            # print(f"{photos['likes']['count']} - {photos['sizes'][2]['url']}")
        pprint(dict_photo)


        directory = 'C:/Users/...../Save_photo/' # тут полный путь к папке с фотками
        list_photo = []
        if sorted(dict_photo)[len(sorted(dict_photo)) - 1] in dict_photo.keys():
            URL_PHOTO = dict_photo[sorted(dict_photo)[len(sorted(dict_photo)) - 1]]
            urllib.request.urlretrieve(URL_PHOTO, f"{directory}{sorted(dict_photo)[len(sorted(dict_photo)) - 1]}.jpg")
            list_photo.append(sorted(dict_photo)[len(sorted(dict_photo)) - 1])

        if 3 < len(sorted(dict_photo)) > 1 and sorted(dict_photo)[len(sorted(dict_photo)) - 2] in dict_photo.keys():

            URL_PHOTO = dict_photo[sorted(dict_photo)[len(sorted(dict_photo)) - 2]]
            urllib.request.urlretrieve(URL_PHOTO, f"{directory}{sorted(dict_photo)[len(sorted(dict_photo)) - 2]}.jpg")
            list_photo.append(sorted(dict_photo)[len(sorted(dict_photo)) - 2])

        if 4 < len(sorted(dict_photo)) > 2 and sorted(dict_photo)[len(sorted(dict_photo)) - 3] in dict_photo.keys():

            URL_PHOTO = dict_photo[sorted(dict_photo)[len(sorted(dict_photo)) - 3]]
            urllib.request.urlretrieve(URL_PHOTO, f"{directory}{sorted(dict_photo)[len(sorted(dict_photo)) - 3]}.jpg")
            list_photo.append(sorted(dict_photo)[len(sorted(dict_photo)) - 3])
        else:
            print('нет больше фото')
        print(sorted(list_photo))
        return list_photo



def get_info_owner(access_token, id_user='13708102'):

    URl = 'https://api.vk.com/method/users.get'
    params = {'access_token': access_token, 'fields': 'bdate,sex,city,domain',
              'user_ids': randrange(10 ** 7), 'v': '5.131'}
    res = requests.get(URl, params=params, )
    pprint(res.json())
    pprint(f"https://vk.com/{res.json()['response'][0]['domain']}")
    return f"{res.json()['response'][0]['first_name']} {res.json()['response'][0]['last_name']}\nhttps://vk.com/{res.json()['response'][0]['domain']}"
if __name__ == '__main__':
    load_dotenv(find_dotenv())
    # get_info_owner(os.getenv('VK_MYTOKEN'))
    print(get_photo(os.getenv('VK_MYTOKEN')))
    for img in get_photo(os.getenv('VK_MYTOKEN')):
        print(img)

# if len(res.json()['response']['items']) > 0:
#     for photos in res.json()['response']['items']:
#         dict_photo[photos['likes']['count'], photos['id']] = photos['sizes'][2]['url']
#         # print(f"{photos['likes']['count']} - {photos['sizes'][2]['url']}")
#     pprint(dict_photo)
#
#     directory = 'C:/Users/nikoanna/Desktop/Командный курсовой/Save_photo/'  # тут полный путь к папке с фотками
#     list_photo = []
#     if sorted(dict_photo)[len(sorted(dict_photo)) - 1] in dict_photo.keys():
#         URL_PHOTO = dict_photo[sorted(dict_photo)[len(sorted(dict_photo)) - 1]]
#         urllib.request.urlretrieve(URL_PHOTO, f"{directory}{sorted(dict_photo)[len(sorted(dict_photo)) - 1]}.jpg")
#         list_photo.append(sorted(dict_photo)[len(sorted(dict_photo)) - 1])
#
#     if 3 < len(sorted(dict_photo)) > 1 and sorted(dict_photo)[len(sorted(dict_photo)) - 2] in dict_photo.keys():
#         URL_PHOTO = dict_photo[sorted(dict_photo)[len(sorted(dict_photo)) - 2]]
#         urllib.request.urlretrieve(URL_PHOTO, f"{directory}{sorted(dict_photo)[len(sorted(dict_photo)) - 2]}.jpg")
#         list_photo.append(sorted(dict_photo)[len(sorted(dict_photo)) - 2])
#
#     if 4 < len(sorted(dict_photo)) > 2 and sorted(dict_photo)[len(sorted(dict_photo)) - 3] in dict_photo.keys():
#
#         URL_PHOTO = dict_photo[sorted(dict_photo)[len(sorted(dict_photo)) - 3]]
#         urllib.request.urlretrieve(URL_PHOTO, f"{directory}{sorted(dict_photo)[len(sorted(dict_photo)) - 3]}.jpg")
#         list_photo.append(sorted(dict_photo)[len(sorted(dict_photo)) - 3])
#     else:
#         print('нет больше фото')
#     print(sorted(list_photo))
#     return list_photo
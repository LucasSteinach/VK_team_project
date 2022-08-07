from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
import os
from dotenv import load_dotenv, find_dotenv

from check_app import get_info_owner, get_photo
load_dotenv(find_dotenv())

vk = vk_api.VkApi(token=os.getenv('KEY_VKinderPy'))
longpoll = VkLongPoll(vk)



upload = VkUpload(vk)

def write_msg(user_id, message): #ответ без вложения
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})

def write_msg_attachment(user_id, message):

    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7), 'attachment': 'photo5897975_456239039, photo5897975_375082758, photo5897975_373390396'})

if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text

                if request == "привет":
                    write_msg_attachment(event.user_id, f"Хай, Вот,что мы подобрали для вас!\n{get_info_owner(os.getenv('VK_MYTOKEN'), event.user_id)}")

                elif request == "пока":
                    write_msg(event.user_id, "Пока((")
                else:
                    write_msg(event.user_id, "Не поняла вашего ответа...")
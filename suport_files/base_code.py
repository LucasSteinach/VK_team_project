import os
from dotenv import load_dotenv, find_dotenv
from requests_info_vk_fun import get_info_owner, get_photo, get_info_bot_user, compare_parametrs
from pprint import pprint
import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
from send_fun import write_msg, write_msg_attachment


load_dotenv(find_dotenv())
vk = vk_api.VkApi(token=os.getenv('KEY_VKinderPy'))

longpoll = VkLongPoll(vk)

upload = VkUpload(vk)
if __name__ == '__main__':

    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text.lower()
                print(event.user_id)
                info_bot_user = get_info_bot_user(os.getenv('VK_MYTOKEN'), event.user_id)

                if request == "привет":

                    comparison = compare_parametrs(os.getenv('VK_MYTOKEN'), info_bot_user)
                    attachments = get_photo(os.getenv('VK_MYTOKEN'), comparison['response'][0]['id'])

                    write_msg_attachment(event.user_id, f"Привет!, Вот,что мы подобрали для вас!\n"
                                                        f"{comparison['response'][0]['first_name']}"
                                                        f" {comparison['response'][0]['last_name']}\n"
                                                        f"https://vk.com/{comparison['response'][0]['domain']}",
                                         vk_authoriz=vk, attachments=attachments)


                elif request == "пока":
                    write_msg(event.user_id, "Пока((", vk_authoriz=vk)
                else:
                    write_msg(event.user_id, "Не знаю, что на это ответить(...", vk_authoriz=vk)

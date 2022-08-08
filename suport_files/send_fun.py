
from random import randrange

#ответ без вложения
def write_msg(user_id, message,vk_authoriz):
    vk_authoriz.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})


def write_msg_attachment(user_id, message, vk_authoriz, attachments):

    vk_authoriz.method(
        'messages.send', {
            'user_id': user_id,
            'message': message,
            'random_id': randrange(10 ** 7),
            'attachment': attachments
        }
    )
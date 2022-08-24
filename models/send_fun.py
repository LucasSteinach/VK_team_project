from random import randrange

#ответ без вложения
def write_msg(user_id, message, vk_authoriz, keyboard=None):
    """
        Функция отправки сообщения пользователю
        :param user_id ID пользователя
        :type user_id: int

        :param message Сообщение, отправляемое пользователю бота
        :type message: str

        :param vk_authoriz Экземпляр класса VKApi
        :param keyboard Клавиатура пользователя для действий с ботом формируется из
        метода get_keyboard класса VkKeyboard, возвращается в формате json.
    """
    vk_authoriz.method('messages.send',
                       {'user_id': user_id,
                        'message': message,
                        'random_id': randrange(10 ** 7),
                        'keyboard': keyboard})


def write_msg_attachment(user_id, message, vk_authoriz, attachments, keyboard=None):
    """
        Функция отправки сообщения пользователю с вложением
        :param user_id ID пользователя
        :type user_id: int

        :param message Сообщение, отправляемое пользователю бота
        :type message: str

        :param vk_authoriz Экземпляр класса VKApi
        :param keyboard Клавиатура пользователя для действий с ботом формируется из
        метода get_keyboard класса VkKeyboard, возвращается в формате json.
        :param attachments Фото найденного человека, отправляемые пользователю бота
        :type attachments: list or str
    """
    vk_authoriz.method(
        'messages.send', {
            'user_id': user_id,
            'message': message,
            'random_id': randrange(10 ** 7),
            'attachment': attachments,
            'keyboard': keyboard

        }
    )
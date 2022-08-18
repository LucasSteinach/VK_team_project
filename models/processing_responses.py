def determine_gender(response_json):
    """
    Функция определяет противоположный пол пользователя.
    :param response_json Информация о пользователе в формате json
    :return Функция возвращает число, соответсвующее значению ключа 'sex' противоположного пола.
    """
    if response_json['response'][0]['sex'] == 1:
        return 2
    elif response_json['response'][0]['sex'] == 2:
        return 1
    else:
        return 0
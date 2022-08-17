

def determine_gender(response_json):
# определяет противоположный пол для ответов полученных методом users.get
# принимает в качестве аргумента словарь (res.json())
# с параметром fields: 'sex'

    if response_json['response'][0]['sex'] == 1:
        return 2
    elif response_json['response'][0]['sex'] == 2:
        return 1
    else:
        return 0

import vk
from tokens import token
import os
from random import randrange
from datetime import date

from pprint import pprint
# from user_token import user_token

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


class vk_api():
    session = vk.Session(access_token=token)
    api = vk.API(session, v='5.89')

    def __init__(self, name):
        self.name = name

    # отправка сообщения с клавиатурой с 2-мя кнопками
    def message_sent(self, user_id, message):
        vk_api.api.messages.send(user_id=str(user_id), message=message,
                                 random_id=randrange(10 ** 7),
                                 keyboard=open(os.path.join(THIS_FOLDER, 'keyboard.json'), "r",
                                               encoding="UTF-8").read())

    # отправка сообщения с пустой клавиатурой для отключения кнопок вк
    def good_bye(self, user_id, message):
        vk_api.api.messages.send(user_id=str(user_id), message=message,
                                 random_id=randrange(10 ** 7),
                                 keyboard=open(os.path.join(THIS_FOLDER, 'empty_keyboard.json'), "r",
                                               encoding="UTF-8").read())

    # получение инф о пользователе с токеном группы
    def get_user_inf(self, user_id):
        fields = 'sex, city, relation, bdate'
        response = vk_api.api.users.get(user_id=str(user_id), fields=fields, v=5.89)
        return response

    # заполнение словаря парамметров для поиска подходящих пользователей
    def get_search_fields(self, response):
        fields_dict = {}
        if response[0]['sex'] == 1:
            fields_dict['sex'] = 2
        else:
            fields_dict['sex'] = 1
        fields_dict['city'] = response[0]['city']['id']
        fields_dict['age'] = self.calculate_age(response[0]['bdate'])
        return fields_dict

    # вычисление возраста пользователя
    def calculate_age(self, bdate):
        today = date.today()
        templist = bdate.split('.')
        born = date(int(templist[2]), int(templist[1]), int(templist[0]))
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    # поиск подходящих пользователей
    def users_search (self, user_token, user_id):
        fields_dict = self.get_search_fields(self.get_user_inf(user_id))
        session = vk.Session(access_token=user_token)
        api = vk.API(session, v='5.89')
        fields = 'relation'
        response = api.users.search(count=1000, fields=fields, city=fields_dict.get('city'),
                                    sex=fields_dict.get('sex'), age_from =fields_dict.get('age')-5,
                                    age_to=fields_dict.get('age'))
        return response


# vk_api = vk_api('vk_api')
# pprint(vk_api.users_search(user_token, 33717265))


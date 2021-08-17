import time
import vk
from tokens import token
import os
from random import randrange
from datetime import date
import json

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


class vk_api():
    session = vk.Session(access_token=token)
    api = vk.API(session, v='5.89')

    def __init__(self, name):
        self.name = name

    # отправка сообщения с клавиатурой с 2-мя кнопками
    def message_send(self, user_id, message):
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

    # отправляем сообщение с клавиатурой с кнопкой токен
    def get_token(self, user_id, message):
        vk_api.api.messages.send(user_id=str(user_id), message=message,
                                 random_id=randrange(10 ** 7),
                                 keyboard=open(os.path.join(THIS_FOLDER, 'token_keyboard.json'), "r",
                                               encoding="UTF-8").read())

    def send_photo(self, user_id, message, attachment):
        vk_api.api.messages.send(user_id=str(user_id), message=message,attachment=attachment,
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
    def users_search(self, user_token, user_id):
        fields_dict = self.get_search_fields(self.get_user_inf(user_id))
        session = vk.Session(access_token=user_token)
        api = vk.API(session, v='5.89')
        fields = 'relation, last_seen'
        time.sleep(0.5)
        response = api.users.search(count=1000, fields=fields, city=fields_dict.get('city'),
                                    sex=fields_dict.get('sex'), age_from=fields_dict.get('age') - 5,
                                    age_to=fields_dict.get('age'), has_photo=1)
        return response

    # производим выборку по результатам поиска
    def get_users_id(self, user_token, user_id):
        response = self.users_search(user_token, user_id)
        id_list = []
        for id in range(0, len(response['items'])):
            # проверяем семейное положение
            if response['items'][id].get('relation') == 1 or response['items'][id].get('relation') == 6:
                # проверяем открыт ли аккаунт
                if response['items'][id].get('is_closed') == False:
                    # проверка аккаунта на заброшенность более чем в 2 недели
                    if time.time() - response['items'][id]['last_seen']['time'] < 1209600:
                        id_list.append(response['items'][id].get('id'))
        return id_list

    # получаем фото
    def get_photo(self, user_token, user_id):
        id_list = self.get_users_id(user_token, user_id)
        session = vk.Session(access_token=user_token)
        api = vk.API(session, v='5.89')
        temp_dict = {}
        ph_dict = {}
        while len(ph_dict.keys()) != 3:
            rand_user = randrange(0, len(id_list))
            time.sleep(0.25)
            response = api.photos.get(owner_id=id_list[rand_user], album_id='profile', extended=1)
            if response['count'] >= 3:
                # получаем ссылку на фото наибольшего разрешения
                for elements in response['items']:
                    ph_size = 0
                    for resolution in elements['sizes']:
                        if resolution['height'] * resolution['width'] > ph_size:
                            ph_size = resolution['height'] * resolution['width']
                            photo_ids = elements['id']
                    temp_dict[photo_ids] = int(elements['likes']['count']) + int(elements['comments']['count'])
                else:
                    pass
            ph_dict[id_list[rand_user]] = temp_dict.copy()
            temp_dict.clear()
        return ph_dict

    # запишем наш словарь с ссылками на фото в файл json
    def write(self, user_token, user_id):
        ph_dict = self.get_photo(user_token, user_id)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(ph_dict, f, ensure_ascii=False, indent=4)

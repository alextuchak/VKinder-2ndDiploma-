from vk_api import vk_api
from photo_send import PhotoSend
from tokens import user_token
import json
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
vk_api = vk_api('vk_api')
photo_send = PhotoSend('send')


class additional_inf():
    def __init__(self, name):
        self.name = name

    # создаем временный файл с полями для поиска
    def dict_create(self, user_id):
        fields_dict = vk_api.get_search_fields(vk_api.get_user_inf(user_id), user_id)
        with open(f'cache{user_id}.json', 'w', encoding='utf-8') as f:
            json.dump(fields_dict, f, ensure_ascii=False, indent=4)

    def json_reader(self, user_id):
        with open(f'cache{user_id}.json') as f:
            fields_dict = json.load(f)
            return fields_dict

    # проверяем наличие недостающей информации
    def inf_check(self, user_id):
        fields_dict = self.json_reader(user_id)
        if fields_dict.get('sex') == 0:
            message = f'Укажите ваш пол:'
            vk_api.user_sex(user_id, message)
            return
        if fields_dict.get('city') == None:
            message = f'Укажите город проживания:'
            vk_api.good_bye(user_id, message)
            return
        if fields_dict.get('age') == None:
            message = f'Укажите дату рождения в формате dd.mm.yyyy:'
            vk_api.good_bye(user_id, message)
            return
        else:
            vk_api.write(user_token, user_id)
            photo_send.photo_send(user_id)

    # дописываем пол пользователя
    def add_sex_inf(self, user_id, sex):
        fields_dict = self.json_reader(user_id)
        if sex == 'Мужской':
            fields_dict['sex'] = 2
        else:
            fields_dict['sex'] = 1
        with open(f'cache{user_id}.json', 'w', encoding='utf-8') as f:
            json.dump(fields_dict, f, ensure_ascii=False, indent=4)
        self.inf_check(user_id)

    # дописываем город пользователя
    def add_city_inf(self, user_id, city):
        fields_dict = self.json_reader(user_id)
        city_id = vk_api.get_city_id(city)
        fields_dict['city'] = city_id
        with open(f'cache{user_id}.json', 'w', encoding='utf-8') as f:
            json.dump(fields_dict, f, ensure_ascii=False, indent=4)
        self.inf_check(user_id)

    # дописываем возраст пользователя
    def add_age_inf(self, user_id, bdate):
        fields_dict = self.json_reader(user_id)
        age = vk_api.calculate_age(bdate, user_id)
        fields_dict['age'] = age
        with open(f'cache{user_id}.json', 'w', encoding='utf-8') as f:
            json.dump(fields_dict, f, ensure_ascii=False, indent=4)
        self.inf_check(user_id)


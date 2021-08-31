from flask import Flask, request, json
from tokens import confirmation_str
from vk_api import vk_api
from add_inf import additional_inf
import os


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

vk_api = vk_api('vk_api')
add_inf = additional_inf('add_inf')



@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route('/', methods=['POST'])
def processing():
    # Распаковываем json из пришедшего POST-запроса
    data = json.loads(request.get_data())
    # Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_str
    elif data['type'] == 'message_new':
        message_checker(data)
        return 'ok'


def message_checker(data):
    user_id = data['object']['from_id']
    user_name = vk_api.get_user_inf(user_id)[0]['first_name']
    if data['object']['text'] == 'Стоп-бот':
        message = f'До новых встреч, {user_name}'
        vk_api.good_bye(user_id, message)
    elif data['object']['text'] == 'Начать':
        message = f'Привет, {user_name}! Для поиска знакомств нажми кнопку "Знакомства". ' \
                  f'Для прекращения работы нажми кнопку "Стоп-бот"'
        vk_api.message_send(user_id, message)
    elif data['object']['text'] == 'Знакомства':
        add_inf.dict_create(user_id)
        add_inf.inf_check(user_id)
    elif data['object']['text'] == 'Мужской' or data['object']['text'] == 'Женский':
        sex = data['object']['text']
        add_inf.add_sex_inf(user_id, sex)
    elif data['object']['text'].count('.') == 2:
        bdate = data['object']['text']
        add_inf.add_age_inf(user_id, bdate)
    elif vk_api.get_city_id(city=data['object']['text']) is not None:
        city = data['object']['text']
        add_inf.add_city_inf(user_id, city)
    else:
        message = f'Привет, {user_name}! Для поиска знакомств нажми кнопку "Знакомства". ' \
                  f'Для прекращения работы нажми кнопку "Стоп-бот"'
        vk_api.message_send(user_id, message)
from flask import Flask, request, json
from tokens import confirmation_str
from vk_api import vk_api
import os
from photo_send import PhotoSend

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

vk_api = vk_api('vk_api')
photo_send = PhotoSend('send')


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
        message = f'Хорошо, {user_name}, остался 1 шаг - отправь мне токен-пользователя.'
        vk_api.good_bye(user_id, message)
    elif len(data['object']['text']) == 85:
        user_token = data['object']['text']
        vk_api.write(user_token, user_id)
        photo_send.photo_send(user_id)
    else:
        message = f'Привет, {user_name}! Для поиска знакомств нажми кнопку "Знакомства". ' \
                  f'Для прекращения работы нажми кнопку "Стоп-бот"'
        vk_api.message_send(user_id, message)






import json
from vk_api import vk_api
import os
from data_base import data_base
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
vk = vk_api('vk')


class PhotoSend:

    def __init__(self, name):
        self.name = name

    def json_reader(self):
        with open('data.json') as f:
            temp = json.load(f)
            return temp

    def users_id_for_send(self):
        temp = self.json_reader()
        users_id_for_send = []
        for k in temp.keys():
            users_id_for_send.append(k)
        return users_id_for_send

    def photo_id_for_send(self):
        temp = self.json_reader()
        photos_id_for_send = []
        for k in temp.values():
            for i in range(0, 3):
                photo_id = (max(k, key=k.get))
                photos_id_for_send.append(photo_id)
                k.pop(photo_id)
        return photos_id_for_send

    def photo_send(self, user_id):
        users_id_for_send = self.users_id_for_send()
        photo_id_for_send = self.photo_id_for_send()
        id = 0
        for i in range(0, 3):
            message = f'Вот что я нашел. Пользователь https://vk.com/id{users_id_for_send[i]}'
            attachment = f'photo{users_id_for_send[i]}_{photo_id_for_send[0 + id]},' \
                         f'photo{users_id_for_send[i]}_{photo_id_for_send[1 + id]},' \
                         f'photo{users_id_for_send[i]}_{photo_id_for_send[2 + id]},'
            vk.send_photo(user_id, message, attachment)
            data_base(user_id,users_id_for_send=users_id_for_send[i])
            id += 3
        os.remove('data.json')
        os.remove(f'cache{user_id}.json')
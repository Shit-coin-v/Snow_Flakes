import telebot

import requests, os

from telebot import types

import json

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

URL = "http://127.0.0.1:8000/api/project/"

# headers = {}         

# response = requests.get('http://127.0.0.1:8000/api/applicationtView/', headers=headers)        

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT'))

# token = '6180857955:AAGyzwyswIgZTd2pO3hSnacpx3XMII0BS0Q'

# bot = telebot.TeleBot(token)

from datetime import datetime


start_keyboard = types.ReplyKeyboardMarkup(True)

create_btn = 'Создать'
project_btn = 'Список проектов'

start_keyboard.add(create_btn)
start_keyboard.add(project_btn)

edit_keyboard = types.ReplyKeyboardMarkup(True)

name = 'Название'
description = 'Описание'
image = 'Фото'

edit_keyboard.add(name)
edit_keyboard.add(description)
edit_keyboard.add(image)



delete_project = 'Удалить'
edit_project = 'Редоктировать'


datas = {}
update_datas = {}



def create_dir():
    dir = os.path.join("media")
    if not os.path.exists(dir):
        os.mkdir(dir)


def get_project():
    return requests.get(URL).json()


@bot.message_handler(commands=["start"])
def send_mess(message):
    bot.send_message(
        message.chat.id, 'привет',
        reply_markup=start_keyboard,
    )


def get_name(message):
    datas['name'] = message.text
    msg = bot.send_message(message.chat.id, 'Введите описание')
    bot.register_next_step_handler(msg, get_description)


def get_description(message):
    description = message.text
    datas['description'] = description
    msg = bot.send_message(message.chat.id, 'Загрузите фото проекта')
    bot.register_next_step_handler(msg, get_documents)
    

def get_documents(message):
    file_name = message.photo[-1].file_id
    file_id_info = bot.get_file(file_name)
    downloaded_file = bot.download_file(file_id_info.file_path)
    
    create_dir()

    image_path = f'./media/document_{datetime.now().strftime("%Y%m%d%H%M%S")}.jpeg'
    datas['image'] = image_path
    with open(image_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_message(message.chat.id, 'Успешно созданено')

    files = {'image': open(datas.pop('image'), 'rb')}

    response = requests.post(URL, datas, files=files)
    print(response.status_code)
    datas.clear()

@bot.message_handler(content_types=["text"])
def get_messages(message):
    if message.text == create_btn:
        msg = bot.send_message(message.chat.id, 'Введите название проекта')
        bot.register_next_step_handler(msg, get_name)
    elif message.text == project_btn:
        json_project = get_project()
        for i in json_project:
            markup = types.InlineKeyboardMarkup()
            edit_btn = types.InlineKeyboardButton('Редоктировать', callback_data=f'Редоктировать {i["id"]}')
            dlt_btn = types.InlineKeyboardButton('Удалить', callback_data=f'Удалить {i["id"]}')
            markup.add(edit_btn)
            markup.add(dlt_btn)
            msg = f"{i['name']}\n\n{i['description']}\n\n{i['image']}"
            bot.send_message(message.chat.id, msg, reply_markup=markup)
    elif message.text == project_btn:
        if project_btn == []:
            bot.send_message(message.chat.id, 'В базе данных нет проектов')
    elif message.text == name:
        msg = bot.send_message(message.chat.id, 'Введите новое название для этого проекта')
        bot.register_next_step_handler(msg, update_name)
    elif message.text == description:
        msg = bot.send_message(message.chat.id, 'Введите новое описание для этого проекта')
        bot.register_next_step_handler(msg, update_description)
    elif message.text == image:
        msg = bot.send_message(message.chat.id, 'Загрузите новое фото проекта')
        bot.register_next_step_handler(msg, update_image)


def del_project(id_project, message):
    response = requests.delete(f'{URL}{id_project}/')
    status = response.status_code
    if status == 404:
        bot.send_message(message.chat.id, 'Такого проекта не существует')
    else:
        bot.send_message(message.chat.id, f'Проект {id_project} успешно удален')


def edit_proj(id_project, data, message):
    response = requests.patch(f'{URL}{id_project}/', data)
    status = response.status_code
    if status == 404:
        bot.send_message(message.chat.id, 'Такого проекта не существует')
    else:
        bot.send_message(message.chat.id, f'Проект {id_project} успешно редоктирован')

def update_progect_image(id_project, files, message):
    response = requests.patch(f'{URL}{id_project}/', {}, files=files)
    sc = response.status_code
    if sc == 404:
        bot.send_message(message.chat.id, 'Такого проекта не существует')
    else:
        bot.send_message(message.chat.id, f'Проект {id_project} успешно редоктирован')


def update_name(message):
    update_datas['name'] = message.text
    edit_proj(update_datas.pop('id'), update_datas, message)
    update_datas.clear()
    bot.send_message(message.chat.id, 'Название изменено', reply_markup=start_keyboard)


def update_description(message):
    update_datas['description'] = message.text
    edit_proj(update_datas.pop('id'), update_datas, message)
    update_datas.clear()
    bot.send_message(message.chat.id, 'Описание изменено', reply_markup=start_keyboard)

def update_image(message):
    file_name = message.photo[-1].file_id
    file_id_info = bot.get_file(file_name)
    downloaded_file = bot.download_file(file_id_info.file_path)
    
    create_dir()

    image_path = f'./media/document_{datetime.now().strftime("%Y%m%d%H%M%S")}.jpeg'
    update_datas['image'] = image_path
    with open(image_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    files = {'image': open(update_datas.pop('image'), 'rb')}

    update_progect_image(update_datas.pop('id'), files, message)

    update_datas.clear()
    os.remove(image_path)
    bot.send_message(message.chat.id, 'Фото успешно изменено', reply_markup=start_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if delete_project in call.data:
        ids = call.data.split(' ')[1]
        del_project(ids, call.message)
    elif edit_project  in call.data:
        update_datas['id'] = call.data.split(' ')[1]
        bot.send_message(call.message.chat.id, 'Что хотите редактировать название, описание или фото проекта?', reply_markup=edit_keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)
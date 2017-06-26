# -*- coding: utf-8 -*-?
import telebot
import time

import requests.exceptions as r_exceptions
from requests import ConnectionError

from Brif import const, base, markups, temp, config

bot = telebot.TeleBot(config.token)
uploaded_items = {}


# Обработка /start команды - ветвление пользователей на покупателя и продавца
@bot.message_handler(commands=['start'])
def start(message):
    base.add_user(message)
    bot.send_message(message.chat.id, const.welcome, reply_markup=markups.start())


# Добавление заявки.

# Добавление имени
@bot.callback_query_handler(func=lambda call: call.data == 'add_item')
def handle_add_item_type(call):
    new_item = temp.Item()
    const.new_items_user_adding.update([(call.message.chat.id, new_item)])
    sent = bot.send_message(call.message.chat.id, "Как мы можем к Вам обращаться?")
    bot.register_next_step_handler(sent, base.add_item_type)
    const.user_adding_item_step.update([(call.message.chat.id, "Enter name")])


# Добавление почты
@bot.message_handler(func=lambda message: base.get_user_step(message.chat.id) == "Enter name")
def handle_add_item_name(message):
    sent = bot.send_message(message.chat.id, "Введите e-mail")
    bot.register_next_step_handler(sent, base.add_item_name)
    const.user_adding_item_step[message.chat.id] = "Enter company"


# Выбор назначения
@bot.message_handler(func=lambda message: base.get_user_step(message.chat.id) == "Enter company")
def handle_add_item_company(message):
    sent = bot.send_message(message.chat.id, "Назначение помещения", reply_markup=markups.naznachenie())
    bot.register_next_step_handler(sent, base.add_item_company)
    const.user_adding_item_step[message.chat.id] = "Enter price"


# Выбор состояния
@bot.message_handler(func=lambda message: base.get_user_step(message.chat.id) == "Enter price")
def handle_add_item_price(message):
    sent = bot.send_message(message.chat.id, "Состояние", reply_markup=markups.sostoyanie())
    bot.register_next_step_handler(sent, base.add_item_price)
    const.user_adding_item_step[message.chat.id] = "Enter description"


# Добавление площади
@bot.message_handler(func=lambda message: base.get_user_step(message.chat.id) == "Enter description")
def handle_add_item_description(message):
    sent = bot.send_message(message.chat.id, "Площадь м2")
    bot.register_next_step_handler(sent, base.add_item_description)
    const.user_adding_item_step[message.chat.id] = "Enter URL"


# Добавление кол-ва комнат
@bot.message_handler(func=lambda message: base.get_user_step(message.chat.id) == "Enter URL")
def handle_add_item_url(message):
    sent = bot.send_message(message.chat.id, "Количество комнат")
    bot.register_next_step_handler(sent, base.add_item_url)
    const.user_adding_item_step[message.chat.id] = "Enter wc"


# Добавление кол-ва санузлов
@bot.message_handler(func=lambda message: base.get_user_step(message.chat.id) == "Enter wc")
def handle_add_item_wc(message):
    sent = bot.send_message(message.chat.id, "Количество санузлов")
    bot.register_next_step_handler(sent, base.add_item_wc)
    const.user_adding_item_step[message.chat.id] = "End"


# Конец добавления заявки
@bot.message_handler(func=lambda message: base.get_user_step(message.chat.id) == "End")
def handle_add_item_end(message):
    bot.send_message(message.chat.id, "Ваша заявка принята.")
    bot.send_message(const.admin_id, base.result)
    const.user_adding_item_step.pop(message.chat.id)


# Запуск бота

while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except ConnectionError as expt:
        config.log(Exception='HTTP_CONNECTION_ERROR', text=expt)
        print('Connection lost..')
        time.sleep(30)
        continue
    except r_exceptions.Timeout as exptn:
        config.log(Exception='HTTP_REQUEST_TIMEOUT_ERROR', text=exptn)
        time.sleep(5)
        continue
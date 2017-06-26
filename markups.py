# -*- coding: utf-8 -*-?
import telebot
from Brif import temp, base


def start():
    markup = telebot.types.InlineKeyboardMarkup()
    btn_user = telebot.types.InlineKeyboardButton(text="Да!", callback_data='add_item')
    markup.add(btn_user)
    return markup

def naznachenie():
    markup = telebot.types.ReplyKeyboardMarkup(True, True)
    markup.row("Квартира для постоянного проживания", "Квартира живу время от времени")
    markup.row("Коттедж для постоянного проживания", "Коттедж для летнего отдыха или по выходным")
    markup.row("Офис", "Ресторан")
    return markup

def sostoyanie():
    markup = telebot.types.ReplyKeyboardMarkup(True, True)
    markup.row("Есть старый ремонт", "Новостройка, стен нет")
    markup.row("Новостройка, стены есть", "Требуется перепланировка")
    markup.row("Другое")
    return markup

def add_item():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for category in base.give_menu():
        markup.add(category)
    return markup

def remove_reply_keyboard():
    markup = telebot.types.ReplyKeyboardRemove()
    return markup
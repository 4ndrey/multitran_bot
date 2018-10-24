# -*- coding: utf-8 -*-
import os
import telebot
from multitran_api import *

# Config vars
token = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, 'Hallo! Geben Sie ein Wort zu übersetzen')

# Translate any text message
@bot.message_handler(func=lambda message: True, content_types=['text'])
def remember_message(message):
    bot.send_message(message.chat.id, multitran_translate(message.text))

bot.polling()

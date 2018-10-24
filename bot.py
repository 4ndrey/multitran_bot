# -*- coding: utf-8 -*-
import os
import telebot
import re
import time
import json

# Config vars
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)

from urllib import parse

import urllib
import requests
from urllib.parse import quote
from lxml import etree

def translate(message):
    result = multitran(message.text)
    bot.send_message(message.chat.id, result)

def multitran(word):
    word = quote(word)
    page = 'http://www.multitran.ru/c/m.exe?CL=1&s=%s&l1=%d'%(word, 3)
    r = requests.get(page)
    r.encoding = 'cp1251'
    page = r.text
    translation = ''
    html = etree.HTML(page)
    trs = html.xpath('//form[@id="translation"]/../table[2]/tr')
    for tr in trs:
        tds = tr.xpath('td')
        line = ''
        for td in tds:
            for elem in td.xpath('descendant::text()'):
                s = elem.rstrip('\r\n')
                line += '%s' % s
        line = line.strip()
        translation += line.split('|', 1)[0] + '\n'
        if 'общ.' in line:
            break
    return translation.replace('общ.', '\n')

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, 'Type word to translate')

@bot.message_handler(func=lambda message: True, content_types=['text'])
def remember_message(message):
    translate(message)

bot.polling()

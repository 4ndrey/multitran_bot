# -*- coding: utf-8 -*-
# import urllib
import requests
from urllib.parse import quote
from lxml import etree

lang = 3 #de

def multitran_translate(text):
    url = 'http://www.multitran.ru/c/m.exe?CL=1&s=%s&l1=%d'%(quote(text), lang)

    r = requests.get(url)
    r.encoding = 'cp1251'
    page = r.text

    translation = ''
    html = etree.HTML(page)
    trs = html.xpath('//form[@id="translation"]/../table[2]/tr')
    for tr in trs:
        line = ''
        for td in tr.xpath('td'):
            for elem in td.xpath('descendant::text()'):
                line += '%s' % elem.rstrip('\r\n')

        # make some cleanups
        line = line.strip()
        translation += line.split('|', 1)[0] + '\n'

        if 'общ.' in line: # stop if general meaning is found
            translation = translation.replace('общ.', '\n')
            break

    return translation

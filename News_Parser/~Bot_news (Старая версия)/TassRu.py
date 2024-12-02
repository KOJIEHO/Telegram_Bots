import requests
import sqlite3
from user_id import user_id, token
import telebot
from Dictionary import words, bad_words, words_seed, words_neft, words_price
import json
import datetime
import telebot
from make_percent import similarity
from universal_DB_connection import DB_maker

bot = telebot.TeleBot(token)
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/100.0.4896.75 Safari/537.36',
    'accept': '*/*'}
proxies = {'https' : 'http://6aU3FV:AUdWm2@194.93.26.1:8000'}

# Получение ссылок и заголовков
#################################################################################################
def get_info_TassRu(url):
    global link, header
    r = requests.get(url, headers=headers, proxies=proxies).text
    b = json.loads(r)

    link = []
    header = []
    for el in (b['data']['news']):
        link.append(el['link'])
        header.append(el['title'])
    link = [link[0]]
    date0 = str(datetime.datetime.now())[:16]
    header = [date0 + '\n' + header[0]]
    return link, header
#################################################################################################

# Основная часть
##################################################################################################
def main_TassRu():
    # try:
        get_info_TassRu("https://tass.ru/live/api/v1/get_feed?timestamp=9999999999&limit=50")
        DB_maker('TassRu', link[0], header[0])
    # except:
    #     pass
##################################################################################################
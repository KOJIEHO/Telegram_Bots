import requests
import sqlite3
from user_id import user_id, token
import telebot
from bs4 import BeautifulSoup
import datetime
from Dictionary import words, bad_words, words_seed, words_neft, words_price
from make_percent import similarity
from universal_DB_connection import DB_maker

bot = telebot.TeleBot(token)
URL_KommersantRu1 = 'https://www.kommersant.ru/rubric/3?from=burger'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}

# Ссылки
##################################################################################################
def get_links_KommersantRu():
    global link_KommersantRu

    link_KommersantRu = 0
    response = requests.get(URL_KommersantRu1, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    link_KommersantRu = [
        a.get('href')
        for a in soup.find_all('a')
        if a.get('href') and a.get('href').startswith('')
    ]
    link_KommersantRu = link_KommersantRu[85:86]
    link_KommersantRu[0] = 'https://www.kommersant.ru' + link_KommersantRu[0]

    return link_KommersantRu
##################################################################################################

# Заголовки
##################################################################################################
def get_headers_KommersantRu():
    global header_KommersantRu

    response = requests.get(str(link_KommersantRu[0]), timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    date0 = str(datetime.datetime.now())[:16]
    header0 = soup.find("h1").text
    header0 = " ".join(header0.split())
    header_KommersantRu = [str(date0) + '\n' + header0]

    return header_KommersantRu
##################################################################################################

# Основная часть
##################################################################################################
def main_KommersantRu():
    get_links_KommersantRu()
    get_headers_KommersantRu()
    DB_maker('KommersantRu', link_KommersantRu[0], header_KommersantRu[0])
##################################################################################################
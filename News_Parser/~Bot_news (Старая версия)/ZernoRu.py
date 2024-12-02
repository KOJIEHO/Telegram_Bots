import requests
import sqlite3
from user_id import user_id, token
import telebot
from bs4 import BeautifulSoup
import asyncio
from Dictionary import words, bad_words, words_seed, words_neft, words_price
from make_percent import similarity
from universal_DB_connection import DB_maker

bot = telebot.TeleBot(token)
URL_zerno1 = 'https://zerno.ru/news_list?page='
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}

# Ссылки
##################################################################################################
def get_links_ZernoRu():
    global link_ZernoRu

    response = requests.get(URL_zerno1, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    link_ZernoRu = [
        a.get('href')
        for a in soup.find_all('a')
        if a.get('href') and a.get('href').startswith('/node')
    ]
    del0 = link_ZernoRu.pop(0)
    link_ZernoRu = link_ZernoRu[0:1]
    link_ZernoRu[0] = 'https://zerno.ru' + link_ZernoRu[0]

    return link_ZernoRu
##################################################################################################

# Заголовки
##################################################################################################
def get_headers_ZernoRu():
    global header_ZernoRu

    response = requests.get(str(link_ZernoRu[0]), timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    header_ZernoRu = [
        el.text
        for el in soup.select(".field-content")
    ]
    header_ZernoRu = header_ZernoRu[0:2]
    header_ZernoRu[0] = header_ZernoRu[0] + '\n' + header_ZernoRu[1]

    return header_ZernoRu
##################################################################################################

# Основная часть
##################################################################################################
def main_ZernoRu():
    get_links_ZernoRu()
    get_headers_ZernoRu()
    DB_maker('ZernoRu', link_ZernoRu[0], header_ZernoRu[0])
##################################################################################################
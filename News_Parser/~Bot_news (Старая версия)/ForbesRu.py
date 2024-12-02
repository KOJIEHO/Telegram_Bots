import requests
import datetime
import sqlite3
from user_id import user_id, token
import telebot
from bs4 import BeautifulSoup
from Dictionary import words, bad_words, words_seed, words_neft, words_price
from make_percent import similarity
from universal_DB_connection import DB_maker

bot = telebot.TeleBot(token)
URL_ForbesRu = 'https://www.forbes.ru'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}

# Ссылки
##################################################################################################
def get_links_ForbesRu():
    global link_ForbesRu

    response = requests.get(URL_ForbesRu, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    link_ForbesRu = [
        a.get('href')
        for a in soup.find_all('a')
        if a.get('href') and a.get('href')
    ]
    link_ForbesRu = link_ForbesRu[7:8]
    link_ForbesRu[0] = 'https://www.forbes.ru' + link_ForbesRu[0]

    return link_ForbesRu
##################################################################################################

# Заголовки
#################################################################################################
def get_headers_ForbesRu():
    global header_ForbesRu

    response = requests.get(str(link_ForbesRu[0]), timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    header0 = soup.find("h1", {"class": "_1yxU8"}).text
    header0 = " ".join(header0.split())
    date0 = str(datetime.datetime.now())[:16]
    header_ForbesRu = [date0 + '\n' + header0]

    return header_ForbesRu
#################################################################################################

# Основная часть
##################################################################################################
def main_ForbesRu():
    get_links_ForbesRu()
    get_headers_ForbesRu()
    DB_maker('ForbesRu', link_ForbesRu[0], header_ForbesRu[0])
##################################################################################################
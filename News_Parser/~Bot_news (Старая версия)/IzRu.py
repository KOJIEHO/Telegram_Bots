import requests
import sqlite3
from user_id import user_id, token
import telebot
from bs4 import BeautifulSoup
from Dictionary import words, bad_words, words_seed, words_neft, words_price
from make_percent import similarity
from universal_DB_connection import DB_maker

bot = telebot.TeleBot(token)
URL_IzRu1 = 'https://iz.ru/feed'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}

# Ссылки
##################################################################################################
def get_links_IzRu():
    global link_IzRu

    response = requests.get(URL_IzRu1, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    link_IzRu = [
        a.get('href')
        for a in soup.find_all('a')
        if a.get('href') and a.get('href').startswith('')
    ]
    link_IzRu = link_IzRu[70:71]
    link_IzRu[0] = 'https://iz.ru' + link_IzRu[0]

    return link_IzRu
##################################################################################################

# Заголовки
##################################################################################################
def get_headers_IzRu():
    global header_IzRu

    response = requests.get(str(link_IzRu[0]), timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    date0 = soup.find("div", {"class": "article_page__left__top__time__label"}).text
    date0 = " ".join(date0.split())
    header0 = soup.find("h1").text
    header0 = " ".join(header0.split())
    header_IzRu = [date0 + '\n' + header0]

    return header_IzRu
##################################################################################################

# Основная часть
##################################################################################################
def main_IzRu():
    get_links_IzRu()
    get_headers_IzRu()
    DB_maker('IzRu', link_IzRu[0], header_IzRu[0])
##################################################################################################
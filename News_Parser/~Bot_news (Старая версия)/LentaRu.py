import requests
import sqlite3
from user_id import user_id, token
import telebot
from bs4 import BeautifulSoup
from Dictionary import words, bad_words, words_seed, words_neft, words_price
from make_percent import similarity
from universal_DB_connection import DB_maker

bot = telebot.TeleBot(token)
URL_LentaRu1 = 'https://lenta.ru/rubrics/economics/economy/'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}

# Ссылки
##################################################################################################
def get_links_LentaRu():
    global link_LentaRu

    response = requests.get(URL_LentaRu1, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    link_LentaRu = [
        a.get('href')
        for a in soup.find_all('a')
        if a.get('href') and a.get('href').startswith('/news/')
    ]
    link_LentaRu = link_LentaRu[0:1] # 30 на странице
    link_LentaRu[0] = 'https://lenta.ru' + link_LentaRu[0]

    return link_LentaRu
##################################################################################################

# Заголовки
##################################################################################################
def get_headers_LentaRu():
    global header_LentaRu

    response = requests.get(str(link_LentaRu[0]), timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    date0 = soup.find("time", {"class": "topic-header__item topic-header__time"}).text
    date0 = " ".join(date0.split())
    header0 = soup.find("h1").text
    header0 = " ".join(header0.split())
    header_LentaRu = [date0 + '\n' + header0]

    return header_LentaRu
##################################################################################################

# Основная часть
##################################################################################################
def main_LentaRu():
    get_links_LentaRu()
    get_headers_LentaRu()
    DB_maker('LentaRu', link_LentaRu[0], header_LentaRu[0])
##################################################################################################
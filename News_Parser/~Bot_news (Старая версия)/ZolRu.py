import requests
import sqlite3
from user_id import user_id, token
import telebot
from bs4 import BeautifulSoup
from Dictionary import words, bad_words, words_seed, words_neft, words_price
from make_percent import similarity
from universal_DB_connection import DB_maker

bot = telebot.TeleBot(token)
URL_ZolRu1 = 'https://www.zol.ru/news/grain/'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}
# Ссылки
##################################################################################################
def get_links_ZolRu():
    global link_ZolRu

    response = requests.get(URL_ZolRu1, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    link_ZolRu = [
        a.get('href')
        for a in soup.find_all('a')
        if a.get('href') and a.get('href').startswith('/n/')
    ]
    link_ZolRu = link_ZolRu[0:1]
    link_ZolRu[0] = 'https://www.zol.ru' + link_ZolRu[0]

    return link_ZolRu
##################################################################################################

# Заголовки
##################################################################################################
def get_headers_ZolRu():
    global header_ZolRu

    response = requests.get(str(link_ZolRu[0]), timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    date0 = soup.find("div", {"class": "new-news-date news_one_date"}).text
    date0 = " ".join(date0.split())
    header0 = soup.find("h1").text
    header_ZolRu = [date0 + '\n' + header0]

    return header_ZolRu
##################################################################################################

# Основная часть
##################################################################################################
def main_ZolRu():
    get_links_ZolRu()
    get_headers_ZolRu()
    DB_maker('ZolRu', link_ZolRu[0], header_ZolRu[0])
##################################################################################################
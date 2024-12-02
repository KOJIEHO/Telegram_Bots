import requests
import sqlite3
from user_id import user_id, token
import telebot
from bs4 import BeautifulSoup
from Dictionary import words, bad_words, words_seed, words_neft, words_price
from make_percent import similarity
from universal_DB_connection import DB_maker

bot = telebot.TeleBot(token)
URL_OilWorldRu1 = 'https://www.oilworld.ru/news/all?page='
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}

# Ссылки
##################################################################################################
def get_links_OilWorldRu():
    global link_OilWorldRu

    response = requests.get(URL_OilWorldRu1, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    link_OilWorldRu = [
        a.get('href')
        for a in soup.find_all('a')
        if a.get('href') and a.get('href').startswith('')
    ]
    link_OilWorldRu = link_OilWorldRu[63:64]
    link_OilWorldRu[0] = 'https://www.oilworld.ru' + link_OilWorldRu[0]

    return link_OilWorldRu
##################################################################################################

# Заголовки
##################################################################################################
def get_headers_OilWorldRu():
    global header_OilWorldRu

    response = requests.get(str(link_OilWorldRu[0]), timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    date0 = soup.find("span", {"class": "n-date"}).text[:17]
    header0 = soup.find("h2").text
    header_OilWorldRu = [date0 + '\n' + header0]

    return header_OilWorldRu
##################################################################################################

# Основная часть
##################################################################################################
def main_OilWorldRu():
    get_links_OilWorldRu()
    get_headers_OilWorldRu()
    DB_maker('OilWorldRu', link_OilWorldRu[0], header_OilWorldRu[0])
##################################################################################################
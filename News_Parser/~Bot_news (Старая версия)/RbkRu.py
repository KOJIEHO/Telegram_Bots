import requests
import sqlite3
from user_id import user_id, token
import telebot
from bs4 import BeautifulSoup
from Dictionary import words, bad_words, words_seed, words_neft, words_price
from make_percent import similarity
from universal_DB_connection import DB_maker

bot = telebot.TeleBot(token)
URL_RBKRu1 = 'https://www.rbc.ru/economics/?utm_source=topline'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}

# Ссылки
##################################################################################################
def get_links_RbkRu():
    global link_RbkRu
    response = requests.get(URL_RBKRu1, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    link_RbkRu = [
        a.get('href')
        for a in soup.find_all('a')
        if a.get('href') and a.get('href').startswith('https://www.rbc.ru/')
    ]
    link_RbkRu = link_RbkRu[44:45]

    return link_RbkRu
##################################################################################################

# Заголовки
##################################################################################################
def get_headers_RbkRu():
    global header_RbkRu

    response = requests.get(str(link_RbkRu[0]), timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    date0 = soup.find("time", {"class": "article__header__date"}).text
    date0 = " ".join(date0.split())
    header0 = soup.find("h1").text
    header0 = " ".join(header0 .split())
    header_RbkRu = [date0 + '\n' + header0]
    
    return header_RbkRu
##################################################################################################

# Основная часть
##################################################################################################
def main_RbkRu():
    get_links_RbkRu()
    get_headers_RbkRu()
    DB_maker('RbkRu', link_RbkRu[0], header_RbkRu[0])
##################################################################################################
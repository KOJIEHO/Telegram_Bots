import requests
import sqlite3
from user_id import user_id, token
import telebot
from bs4 import BeautifulSoup
from Dictionary import words, bad_words, words_seed, words_neft, words_price
from make_percent import similarity
from universal_DB_connection import DB_maker

bot = telebot.TeleBot(token)
URL_PrimeRu1 = 'https://1prime.ru/Agriculture/'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}

# Ссылки
##################################################################################################
def get_links_PrimeRu():
    global link_PrimeRu

    response = requests.get(URL_PrimeRu1, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    link_PrimeRu = [
        a.get('href')
        for a in soup.find_all('a')
        if a.get('href') and a.get('href').startswith('/state_regulation/2')
    ]
    link_PrimeRu = link_PrimeRu[0:1]
    link_PrimeRu[0] = 'https://1prime.ru/' + link_PrimeRu[0]

    return link_PrimeRu
##################################################################################################

# Заголовки
#################################################################################################
def get_headers_PrimeRu():
    global header_PrimeRu

    response = requests.get(str(link_PrimeRu[0]), timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    header0 = soup.find("div", {"class": "article-header__title"}).text
    header0 = " ".join(header0.split())
    date0 = soup.find("time", {"class": "article-header__datetime"}).text
    date0 = " ".join(date0.split())
    header_PrimeRu = [date0 + '\n' + header0]

    return header_PrimeRu
#################################################################################################

# Основная часть
##################################################################################################
def main_PrimeRu():
    get_links_PrimeRu()
    get_headers_PrimeRu()
    DB_maker('PrimeRu', link_PrimeRu[0], header_PrimeRu[0])
##################################################################################################
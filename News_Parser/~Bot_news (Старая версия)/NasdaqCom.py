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
URL_NasdaqCom1 = 'https://quote.rbc.ru/tag/NASDAQ'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/100.0.4896.75 Safari/537.36',
    'accept': '*/*'}

# Ссылки
##################################################################################################
def get_links_NasdaqCom():
    global link_NasdaqCom

    response = requests.get(URL_NasdaqCom1, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    link_NasdaqCom = [
        a.get('href')
        for a in soup.find_all('a')
        if a.get('href') and a.get('href').startswith('https://')
    ]
    link_NasdaqCom = link_NasdaqCom[39:40]

    return link_NasdaqCom
##################################################################################################

# Заголовки
##################################################################################################
def get_headers_NasdaqCom():
    global header_NasdaqCom

    response = requests.get(str(link_NasdaqCom[0]), timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    date0 = str(datetime.datetime.now())[:16]
    header0 = soup.find("h1").text
    header0 = " ".join(header0.split())
    header_NasdaqCom = [date0 + '\n' + header0]

    return header_NasdaqCom
##################################################################################################

# Основная часть
##################################################################################################
def main_NasdaqCom():
    get_links_NasdaqCom()
    get_headers_NasdaqCom()
    DB_maker('NasdaqCom', link_NasdaqCom[0], header_NasdaqCom[0])
##################################################################################################
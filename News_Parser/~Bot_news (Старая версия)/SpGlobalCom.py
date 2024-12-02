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
URL_SpGlobalCom1 = 'https://www.spglobal.com/commodityinsights/en/market-insights/latest-news'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}
URL_SpGlobalCom1 = 'https://www.spglobal.com/commodityinsights/en/market-insights/latest-news'
URL_SpGlobalCom2 = 'https://www.spglobal.com/'

# Ссылки
##################################################################################################
def get_links_SpGlobalCom():
    global link_SpGlobalCom

    response = requests.get(URL_SpGlobalCom1, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    link_SpGlobalCom = [
        a.get('href')
        for a in soup.find_all('a')
        if a.get('href') and a.get('href').startswith('/commodityinsights/')
    ]
    link_SpGlobalCom = link_SpGlobalCom[21:22]
    link_SpGlobalCom[0] = 'https://www.spglobal.com/' + link_SpGlobalCom[0]
##################################################################################################

# Заголовки
##################################################################################################
def get_headers_SpGlobalCom():
    global header_SpGlobalCom

    response = requests.get(str(link_SpGlobalCom[0]), timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    date0 = str(datetime.datetime.now())[:16]
    header0 = soup.find("h1").text
    header0 = " ".join(header0.split())
    header_SpGlobalCom = [date0 + '\n' + header0]

    return header_SpGlobalCom
##################################################################################################

# Основная часть
##################################################################################################
def main_SpGlobalCom():
    get_links_SpGlobalCom()
    get_headers_SpGlobalCom()
    DB_maker('SpGlobalCom', link_SpGlobalCom[0], header_SpGlobalCom[0])   
##################################################################################################
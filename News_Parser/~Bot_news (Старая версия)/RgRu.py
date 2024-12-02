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
URL_RgRu1 = 'https://rg.ru/tema/ekonomika'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}

# Ссылки
##################################################################################################
def get_links_RgRu():
    global link_RgRu
    link_RgRu = []
    response = requests.get(URL_RgRu1, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    link_RgRu = [
        a.get('href')
        for a in soup.find_all('a')
        if a.get('href') and a.get('href').startswith('/')
    ]
    link_RgRu = link_RgRu[37:38]
    link_RgRu[0] = 'https://rg.ru' + link_RgRu[0]

    return link_RgRu
##################################################################################################

# Заголовки
##################################################################################################
def get_headers_RgRu():
    global header_RgRu

    response = requests.get(str(link_RgRu[0]), timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    date0 = str(datetime.datetime.now())[:16]
    header0 = soup.find("h1").text
    header0 = " ".join(header0.split())
    header_RgRu = [date0 + '\n' + header0]

    return header_RgRu
##################################################################################################

# Основная часть
##################################################################################################
def main_RgRu():
    try:
        get_links_RgRu()
        get_headers_RgRu()
        DB_maker('RgRu', link_RgRu[0], header_RgRu[0])   
    except Exception:
        pass
##################################################################################################
import requests
import sqlite3
from user_id import user_id, token
import telebot
import datetime
from bs4 import BeautifulSoup
from Dictionary import words, bad_words, words_seed, words_neft, words_price

bot = telebot.TeleBot(token)
URL_Agriculture1 = 'https://www.agriculture.com/'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}

# Ссылки
##################################################################################################
def get_links_AgricultureCom():
    global link_business, link_crops, link_livestock, link_machinery, link_technology, link_sf_blog, link_newswire, link_analysis, link_your_world_in_agriculture, link_news, for_making_header, for_making_link

    for_making_link = ['news/business', 'news/crops', 'news/livestock', 'news/machinery', 'news/technology', 'news/sf-blog', 'markets/newswire', 'markets/analysis', 'markets/your-world-in-agriculture', 'weather/news']
    l = 0
    while l < 10:

        response = requests.get(URL_Agriculture1 + for_making_link[l], timeout=30, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')

        link = [
            a.get('href')
            for a in soup.find_all('a')
            if a.get('href') and a.get('href').startswith('https://www.agriculture.com/') # + for_making_link[l])
        ]

        if l == 0:
            link_business = link[98:99]
        elif l == 1:
            link_crops = link[98:99]
        elif l == 2:
            link_livestock = link[98:99]
        elif l == 3:
            link_machinery = link[98:99]
        elif l == 4:
            link_technology = link[98:99]
        elif l == 5:
            link_sf_blog = link[98:99]
        elif l == 6:
            link_newswire = link[85:86]
        elif l == 7:
            link_analysis = link[85:86]
        elif l == 8:
            link_your_world_in_agriculture = link[85:86]
        elif l == 9:
            link_news = link[84:85]
        l += 1

    for_making_header = [link_business, link_crops, link_livestock, link_machinery, link_technology, link_sf_blog, link_newswire, link_analysis, link_your_world_in_agriculture, link_news]
    return link_business, link_crops, link_livestock, link_machinery, link_technology, link_sf_blog, link_newswire, link_analysis, link_your_world_in_agriculture, link_news, for_making_header, for_making_link
##################################################################################################

# Заголовки
##################################################################################################
def get_headers_AgricultureCom():
    global arr_header

    l = 0
    while l < len(for_making_header):
        i = 0
        while i < len(for_making_header[i]):
            response = requests.get(for_making_header[l][i], timeout=30, headers=headers)
            soup = BeautifulSoup(response.content, 'lxml')

            date0 = str(datetime.datetime.now())[:16]
            header0 = soup.find("h1").text
            if l == 0:
                header_business = [date0 + "\n" + header0]
            elif l == 1:
                header_crops = [date0 + "\n" + header0]
            elif l == 2:
                header_livestock = [date0 + "\n" + header0]
            elif l == 3:
                header_machinery = [date0 + "\n" + header0]
            elif l == 4:
                header_technology = [date0 + "\n" + header0]
            elif l == 5:
                header_sf_blog = [date0 + "\n" + header0]
            elif l == 6:
                header_newswire = [date0 + "\n" + header0]
            elif l == 7:
                header_analysis = [date0 + "\n" + header0]
            elif l == 8:
                header_your_world_in_agriculture = [date0 + "\n" + header0]
            elif l == 9:
                header_news = [date0 + "\n" + header0]
            i += 1
        l += 1
    arr_header = [header_business, header_crops, header_livestock, header_machinery, header_technology, header_sf_blog, header_newswire, header_analysis, header_your_world_in_agriculture, header_news]
    return arr_header
##################################################################################################

# Запись в БД и проверка
##################################################################################################
def db_AgricultureCom():

    for_making_db = ['NewsBusiness', 'NewsCrops', 'NewsLivestock', 'NewsMachinery', 'NewsTechnology',
                     'NewsSfBlog', 'MarketsNewswire', 'MarketsAnalysis', 'MarketsYourWorldInAgriculture',
                     'WeatherNews']
    count_header = 0
    count = 0
    while count_header < len(arr_header):
        print(str(count_header + 1) + ' Новость с AgricultureCom - ' + arr_header[count_header][0])
        count_bad_words = 0
        while count < len(bad_words):
            if arr_header[count_header][0].find(bad_words[count]) != -1:
                count_bad_words = 1  # Если будет хоть одно плохое слово, то равно 1
                break
            count += 1
        i = 0
        count = 0
        if count_bad_words == 0:
            while count < len(words):
                if arr_header[count_header][0].find(words[count]) != -1: # Если будет хоть одно хорошее слово, то публикуем
                    i += 1
                    base = sqlite3.connect('AgricultureCom.db')
                    cur = base.cursor()

                    base.execute('CREATE TABLE IF NOT EXISTS ' + str(for_making_db[count_header]) + '(link, header)')
                    base.commit()
                    cur.execute('INSERT INTO ' + str(for_making_db[count_header]) + ' VALUES(?, ?)', ('0', '0'))
                    base.commit()
                    r = cur.execute('SELECT link FROM ' + str(for_making_db[count_header])).fetchall()

                    if r[0][0] == for_making_header[count_header][0]:
                        print('Новых новостей нет - AgricultureCom' + str(for_making_db[count_header]))
                        print('__________________________________________________________________')
                    else:
                        cur.execute('DELETE FROM ' + str(for_making_db[count_header]))
                        base.commit()
                        cur.execute('INSERT INTO ' + str(for_making_db[count_header]) + ' VALUES(?, ?)', (str(for_making_header[count_header][0]), str(arr_header[count_header][0])))
                        base.commit()
                        print('Новость обновлена')
                        print('__________________________________________________________________')
                        smile = ''
                        count_smile = 0
                        while count_smile < len(words_seed):
                            if arr_header[count_header][0].find(words_seed[count_smile]) >= 0:
                                smile = '🌾'
                            count_smile += 1
                        count_smile = 0
                        while count_smile < len(words_neft):
                            if arr_header[count_header][0].find(words_neft[count_smile]) >= 0:
                                smile = '🛢'
                            count_smile += 1
                        count_smile = 0
                        while count_smile < len(words_price):
                            if arr_header[count_header][0].find(words_price[count_smile]) >= 0:
                                smile = '💰 '
                            count_smile += 1
                        if smile == '':
                            smile = '❗'
                        news = f"{smile}{arr_header[count_header][0]}\nИсточник: [Agriculture.com]({for_making_header[count_header][0]})"
                        id = 0
                        while id < len(user_id):
                            bot.send_message(user_id[id], news, parse_mode='Markdown', disable_web_page_preview=True)
                            id += 1
                    break
                count += 1
            if i == 0:
                print('Новость не прошла проверку - AgricultureCom' + str(for_making_db[count_header]))
                print('__________________________________________________________________')
        else:
            print('Новость не прошла проверку - AgricultureCom' + str(for_making_db[count_header]))
            print('__________________________________________________________________')
        count_header += 1
##################################################################################################

# Основная часть
##################################################################################################
def main_AgricultureCom():
    get_links_AgricultureCom()
    get_headers_AgricultureCom()
    db_AgricultureCom()
##################################################################################################
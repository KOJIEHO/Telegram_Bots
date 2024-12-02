import requests
import sqlite3
from user_id import user_id, token
import telebot
from bs4 import BeautifulSoup
from Dictionary import words, bad_words, words_seed, words_neft, words_price, words_maslo

bot = telebot.TeleBot(token)
URL_RiaRu1 = 'https://ria.ru/'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}

# Ссылки
##################################################################################################
def get_links_RiaRu():
    global for_making_header, for_making_link

    for_making_link = ['economy/', 'category_ceny-na-neft/', 'person_EHlvira_Nabiullina/', 'person_Vladimir_Putin/', 'keyword_pshenica/', 'tag_ehksport_2/', 'tag_thematic_category_Import/', 'tag_neft/', 'tag_gaz_2/', 'tag_prodovolstvie/', 'thematic_category_Logistika/']
    l = 0
    while l < 11:

        response = requests.get(URL_RiaRu1 + for_making_link[l], timeout=30, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')

        link = [
            a.get('href')
            for a in soup.find_all('a')
            if a.get('href') and a.get('href').startswith('https://')
        ]
        link = link[12:13]

        if l == 0:
            link_economy = link
        elif l == 1:
            link_ceny_na_neft = link
        elif l == 2:
            link_EHlvira_Nabiullina = link
        elif l == 3:
            link_Vladimir_Putin = link
        elif l == 4:
            link_pshenica = link
        elif l == 5:
            link_ehksport_2 = link
        elif l == 6:
            link_Import = link
        elif l == 7:
            link_neft = link
        elif l == 8:
            link_az_2 = link
        elif l == 9:
            link_prodovolstvie = link
        elif l == 10:
            link_Logistika = link
        l += 1

    for_making_header = [link_economy, link_ceny_na_neft, link_EHlvira_Nabiullina, link_Vladimir_Putin, link_pshenica, link_ehksport_2, link_Import, link_neft, link_az_2, link_prodovolstvie, link_Logistika]
    return for_making_header, for_making_link
##################################################################################################

# Заголовки
##################################################################################################
def get_headers_RiaRu():
    global arr_header

    l = 0
    while l < len(for_making_header):
        i = 0
        while i < len(for_making_header[i]):
            response = requests.get(str(for_making_header[l][i]), timeout=30, headers=headers)
            soup = BeautifulSoup(response.content, 'lxml')

            date0 = soup.find("div", {"class": "article__info-date"}).text
            header0 = str(soup.find("div", {"class": "article__title"}))
            header0 = header0[28:][:-6]
            if header0 == '':
                header0 = soup.find("h1", {"class": "article__title"}).text

            if l == 0:
                header_economy = [date0 + '\n' + header0]
            elif l == 1:
                header_ceny_na_neft = [date0 + '\n' + header0]
            elif l == 2:
                header_EHlvira_Nabiullina = [date0 + '\n' + header0]
            elif l == 3:
                header_Vladimir_Putin = [date0 + '\n' + header0]
            elif l == 4:
                header_pshenica = [date0 + '\n' + header0]
            elif l == 5:
                header_ehksport_2 = [date0 + '\n' + header0]
            elif l == 6:
                header_Import = [date0 + '\n' + header0]
            elif l == 7:
                header_neft = [date0 + '\n' + header0]
            elif l == 8:
                header_az_2 = [date0 + '\n' + header0]
            elif l == 9:
                header_prodovolstvie = [date0 + '\n' + header0]
            elif l == 10:
                header_Logistika = [date0 + '\n' + header0]
            i += 1
        l += 1
    arr_header = [header_economy, header_ceny_na_neft, header_EHlvira_Nabiullina, header_Vladimir_Putin, header_pshenica, header_ehksport_2, header_Import, header_neft, header_az_2, header_prodovolstvie, header_Logistika]
    return arr_header
##################################################################################################

# Запись в БД и проверка
##################################################################################################
def db_RiaRu():

    for_making_db = ['Economy', 'CategoryCenyNaNeft', 'PersonEHlviraNabiullina', 'PersonVladimirPutin',
                       'KeywordPshenica', 'TagEhksport', 'TagThematicCategoryImport', 'TagNeft',
                       'TagGaz', 'TagProdovolstvie', 'ThematicCategoryLogistika']
    count_header = 0
    count = 0
    while count_header < len(arr_header):
        print(str(count_header + 1) + ' Новость с RiaRu - ' + arr_header[count_header][0])
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
                if arr_header[count_header][0].find(words[count]) != -1:  # Если будет хоть одно хорошее слово, то публикуем
                    i += 1
                    base = sqlite3.connect('RiaRu.db')
                    cur = base.cursor()

                    base.execute('CREATE TABLE IF NOT EXISTS ' + str(for_making_db[count_header]) + '(link, header)')
                    base.commit()
                    cur.execute('INSERT INTO ' + str(for_making_db[count_header]) + ' VALUES(?, ?)', ('0', '0'))
                    base.commit()
                    r = cur.execute('SELECT link FROM ' + str(for_making_db[count_header])).fetchall()

                    if r[0][0] == for_making_header[count_header][0]:
                        print('Новых новостей нет - RiaRu' + str(for_making_db[count_header]))
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
                        while count_smile < len(words_maslo):
                            if header.find(words_maslo[count_smile]) >= 0:
                                smile = '🧈'
                            count_smile += 1
                        count_smile = 0
                        while count_smile < len(words_price):
                            if arr_header[count_header][0].find(words_price[count_smile]) >= 0:
                                smile = '💰 '
                            count_smile += 1
                        if smile == '':
                            smile = '❗'
                        news = f"{smile}{arr_header[count_header][0]}\nИсточник: [Ria.ru]({for_making_header[count_header][0]})"
                        id = 0
                        while id < len(user_id):
                            bot.send_message(user_id[id], news, parse_mode='Markdown', disable_web_page_preview=True)
                            id += 1
                    break
                count += 1
            if i == 0:
                print('Новость не прошла проверку - RiaRu' + str(for_making_db[count_header]))
                print('__________________________________________________________________')
        else:
            print('Новость не прошла проверку - RiaRu' + str(for_making_db[count_header]))
            print('__________________________________________________________________')
        count_header += 1
##################################################################################################

# Основная часть
##################################################################################################
def main_RiaRu():
    try:
        get_links_RiaRu()
        get_headers_RiaRu()
        db_RiaRu()
    except Exception:
        pass
##################################################################################################
import sqlite3
from user_id import user_id, token
import telebot
from Dictionary import words, bad_words, words_seed, words_neft, words_price, name_db, words_gaz, words_maslo
from make_percent import similarity
bot = telebot.TeleBot(token)


def DB_maker(name, link, header):
    print('Новость с ' + str(name) + ' - ' + header)
    base = sqlite3.connect(str(name) + '.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS ' + str(name) + '(link, header)')
    base.commit()
    cur.execute('INSERT INTO ' + str(name) + ' VALUES(?, ?)', ('0', '0'))
    base.commit()
    db_link = cur.execute('SELECT link FROM ' + str(name)).fetchall()

    if db_link[0][0] != link:
        count = 0
        count_bad_words = 0
        while count < len(bad_words):
            if header.find(bad_words[count]) != -1:
                count_bad_words = 1  # Если будет хоть одно плохое слово, то равно 1
                break
            count += 1

        if count_bad_words == 0:
            count = 0
            count_good_words = 0
            while count < len(words):
                if header.find(words[count]) > -1:
                    count_good_words = 1  # Если будет хоть одно хорошее слово, то равно 1
                    break
                count += 1

            if count_good_words == 1:
                count = 0
                max_percent = 0
                while count < len(name_db):
                    base1 = sqlite3.connect(name_db[count] + '.db')
                    cur = base1.cursor()
                    db_header0 = cur.execute('SELECT header FROM ' + name_db[count]).fetchall()
                    db_header1 = db_header0[0][0]
                    percent = similarity(header, db_header1)
                    if max_percent < percent:
                        max_percent = percent
                    count += 1
                if max_percent < 0.6:
                    base = sqlite3.connect(str(name) + '.db')
                    cur = base.cursor()
                    cur.execute('DELETE FROM ' + str(name))
                    base.commit()
                    cur.execute('INSERT INTO ' + str(name) + ' VALUES(?, ?)', (link, header))
                    base.commit()
                    smile = ''
                    count_smile = 0
                    while count_smile < len(words_seed):
                        if header.find(words_seed[count_smile]) >= 0:
                            smile = '🌾'
                        count_smile += 1
                    count_smile = 0
                    while count_smile < len(words_neft):
                        if header.find(words_neft[count_smile]) >= 0:
                            smile = '🛢'
                        count_smile += 1
                    count_smile = 0
                    while count_smile < len(words_gaz):
                        if header.find(words_gaz[count_smile]) >= 0:
                            smile = '🔥'
                        count_smile += 1
                    count_smile = 0
                    while count_smile < len(words_maslo):
                        if header.find(words_maslo[count_smile]) >= 0:
                            smile = '🧈'
                        count_smile += 1
                    count_smile = 0
                    while count_smile < len(words_price):
                        if header.find(words_price[count_smile]) >= 0:
                            smile = '💰'
                        count_smile += 1
                    if smile == '':
                        smile = '❗'
                    news = f"{smile}{header}\nИсточник: [{str(name)}]({link})"
                    # bot.send_message(689331353, news, parse_mode='Markdown', disable_web_page_preview=True)
                    id = 0
                    while id < len(user_id):
                        bot.send_message(user_id[id], news, parse_mode='Markdown', disable_web_page_preview=True)
                        id += 1
                    print('Новость обновлена - ' + str(name))
                    print('__________________________________________________________________')
                else:
                    print('Новость не прошла проверку (Плагиат) - ' + str(name))
                    print('__________________________________________________________________')
            else:
                print('Новость не прошла проверку (Нет хороших слов) - ' + str(name))
                print('__________________________________________________________________')
        else:
            print('Новость не прошла проверку (Плохое слово) - ' + str(name))
            print('__________________________________________________________________')
    else:
        print('Новых новостей нет - ' + str(name))
        print('__________________________________________________________________')
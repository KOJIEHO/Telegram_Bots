import requests
import sqlite3
import telebot
from bs4 import BeautifulSoup
import asyncio


user_id = []
token = ''

bot = telebot.TeleBot(token)
URL_USD = 'https://quote.rbc.ru/ticker/59111'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}


async def check_news_update():
    while True:
        try:
            response = requests.get(URL_USD, timeout=30, headers=headers)
            soup = BeautifulSoup(response.content, 'lxml')
            usd = soup.find("span", {"class": "chart__info__sum"}).text[1:]
            usd = usd.replace(",", ".")
            usd = float(usd)

            base = sqlite3.connect('USD.db')
            cur = base.cursor()
            base.execute('CREATE TABLE IF NOT EXISTS USD(info, info0)')
            base.commit()
            cur.execute('INSERT INTO USD VALUES(?, ?)', ('0', '0'))
            base.commit()
            usd0 = cur.execute('SELECT info FROM USD').fetchall()
            usd0 = usd0[0][0]
            print(str(usd0) + ' Число взято из БД')
            print(str(usd) + " Получили с сайта")
            print('Сравниваем')

            if usd0 != usd:
                if abs(usd0 - usd) >= 0.3:
                    if usd > usd0:
                        line = 'вырос'
                    else:
                        line = 'упал'
                    print('Сообщение отправлено')
                    new = 'Курс USD ' + line + ' до:\n₽' + str(usd)
                    id = 0
                    while id < len(user_id):
                        bot.send_message(user_id[id], new, parse_mode='Markdown', disable_web_page_preview=True)
                        id += 1
                    cur.execute('DELETE FROM USD')
                    base.commit()
                    cur.execute('INSERT INTO USD VALUES(?, ?)', (usd, '0'))
                    base.commit()
                    usd0 = cur.execute('SELECT info FROM USD').fetchall()
                    print(str(usd0[0][0]) + '  Новое число в БД')
                    print('__________________________________________________________________')
                else:
                    print('Изменение незначительно')
                    print('__________________________________________________________________')
            else:
                print('Доллар не поменялся')
                print('__________________________________________________________________')
            await asyncio.sleep(1)
        except Exception:
            continue


if __name__ == '__main__':
    asyncio.run(check_news_update())
    bot.polling(none_stop=True)

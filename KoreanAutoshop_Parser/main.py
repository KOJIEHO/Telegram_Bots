import requests
import sqlite3
from bs4 import BeautifulSoup
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}
url = ['http://api.encar.com/search/car/list/premium?count=true&q=(And.Year.range(201800..202299)._.Mileage.range(10000..70000)._.Hidden.N._.CarType.Y._.Trust.Warranty._.Condition.Inspection._.(Or.FuelType.%EB%94%94%EC%A0%A4._.FuelType.%EA%B0%80%EC%86%94%EB%A6%B0.)_.Transmission.%EC%98%A4%ED%86%A0.)&sr=%7CModifiedDate%7C0%7C50', 'http://api.encar.com/search/car/list/premium?count=true&q=(And.Year.range(201800..202299)._.Mileage.range(10000..70000)._.Hidden.N._.CarType.N._.Trust.Warranty._.Condition.Inspection._.(Or.FuelType.%EB%94%94%EC%A0%A4._.FuelType.%EA%B0%80%EC%86%94%EB%A6%B0.)_.Transmission.%EC%98%A4%ED%86%A0.)&sr=%7CModifiedDate%7C0%7C50']
token = ''
bot = Bot(token)
db = Dispatcher(bot)


@db.message_handler(commands=['start'])
async def new_info_send(message: types.Message):
    print('Добавил нового пользователя')
    user_id = message.chat.id
    base = sqlite3.connect('user_id.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS user_id(info, zeroinfo)')
    base.commit()
    cur.execute('INSERT INTO user_id VALUES(?, ?)', (user_id, 0))
    base.commit()
    base.close()
    while True:
        try:
            base = sqlite3.connect('user_id.db')
            cur = base.cursor()
            id_for_message = cur.execute('SELECT info FROM user_id').fetchall()
            response = requests.get('https://bankiros.ru/currency/cbrf/krw', timeout=30, headers=headers)
            data_html = BeautifulSoup(response.content, 'lxml')
            usd = str(data_html.find("div", {"class": "сurrency-cbr__wrapp-picker"}))
            null_name = usd.find('<span>') + 6
            null_name = usd[null_name:].split(' ')
            course_krw = null_name[0]
            count = 1
            while count < 3:
                print('Страница ' + str(count))
                base = sqlite3.connect('DB' + str(count) + '.db')
                cur = base.cursor()
                base.execute('CREATE TABLE IF NOT EXISTS TABLE' + str(count) + '(Id, Array_photo_links, Model, Badge, FuelType, FormYear, Mileage, OfficeCityState, Price, Manufacturer)')
                base.commit()
                Last_id_from_DB = cur.execute('SELECT Id FROM TABLE' + str(count)).fetchall()
                max_size_db = len(Last_id_from_DB)
                print(Last_id_from_DB)
                Last_id_from_DB = Last_id_from_DB[len(Last_id_from_DB)-1][0]
                response = requests.get(url[count - 1], timeout=30, headers=headers)
                data = response.json()
                Id = str(data['SearchResults'][0]['Id'])
                print(Id)
                count_for_photo = 0
                Array_photo_links = []
                while count_for_photo < len(data['SearchResults'][0]['Photos']):
                    Array_photo_links += ['http://ci.encar.com/carpicture' + str(data['SearchResults'][0]['Photos'][count_for_photo]['location']) + '?impolicy=heightRate&rh=91&cw=122&ch=91&cg=Center&wtmk=http://ci.encar.com/wt_mark/w_mark_03.png&wtmkg=SouthEast&wtmkw=45&wtmkh=12.3']
                    count_for_photo += 1
                Array_photo_links = str(Array_photo_links)
                Manufacturer = str(data['SearchResults'][0]['Manufacturer'])
                Model = str(data['SearchResults'][0]['Model'])
                Badge = str(data['SearchResults'][0]['Badge'])
                FuelType = str(data['SearchResults'][0]['FuelType'])
                FormYear = str(data['SearchResults'][0]['FormYear'])
                Mileage = str(data['SearchResults'][0]['Mileage'])
                OfficeCityState = str(data['SearchResults'][0]['OfficeCityState'])
                Price = str(data['SearchResults'][0]['Price'])
                Price = str(round(int(Price[:-2]) * 10 * float(course_krw)))
                if Last_id_from_DB == Id:
                    print('Новых тачек на странице ' + str(count) + ' нет\n')
                    count += 1
                else:
                    print('Вышла новая тачка\n')
                    if int(max_size_db) > 49:
                        id = 0
                        while id < len(id_for_message):
                            await bot.send_message(id_for_message[id][0], 'Новая партия информации по машинам на странице ' + str(count))
                            await bot.send_document(id_for_message[id][0], document=open('DB' + str(count) + '.db', 'rb'))
                            id += 1
                        cur.execute('DROP TABLE TABLE' + str(count))
                        base.commit()
                        base.execute('CREATE TABLE IF NOT EXISTS TABLE' + str(count) + '(Id, Array_photo_links, Model, Badge, FuelType, FormYear, Mileage, OfficeCityState, Price, Manufacturer)')
                        base.commit()
                    cur.execute('INSERT INTO TABLE' + str(count) + ' VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (Id, Array_photo_links, Model, Badge, FuelType, FormYear, Mileage, OfficeCityState, Price, Manufacturer))
                    base.commit()
                    count += 1
            print('##########################################')
        except Exception:
            continue


executor.start_polling(db, skip_updates=True)

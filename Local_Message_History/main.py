from pyrogram import Client
import configparser
import json
import requests
import os.path
import sys

sys.path.append("PLIB")
config = configparser.ConfigParser()
config.read("settings.ini")

api_hash = config["CONFIG"]["api_hash"]
api_id = config["CONFIG"]["api_id"]
url = config["CONFIG"]["url"]
bulk_count = int(config["CONFIG"]["bulk_count"])


# Поиск минимального id сообщения в БД
def min_id(chat_id):
    response = requests.get(f'{url}/ham/sql/query?$IdsFormat=1', data=f'select id from CHAT where idt = {chat_id}')
    try:  # Обработка ошибки, если вдруг чат еще не создан
        chat_id_ham = json.loads(response.text)['value'][0]['$id']
        response = requests.get('http://localhost:4388/ham/sql/query?$IdsFormat=1', data=f'select min(IDT) as min_ID from MESS where CHAT = {chat_id_ham}')
        try:  # Обработка ошибки, если чат создан, но в нем еще нет сообщений
            min_id = json.loads(response.text)['value'][0]['min_id']
        except Exception as inst:
            min_id = 0
    except Exception as inst:
        min_id = 0 
    return min_id

# Поиск максимального id сообщения в БД
def max_id():
    response = requests.get(f'{url}/ham/sql/query?$IdsFormat=1', data=f'select id from CHAT where idt = {chat_id}')
    try:  # Обработка ошибки, если вдруг чат еще не создан
        chat_id_ham = json.loads(response.text)['value'][0]['$id']
        response = requests.get('http://localhost:4388/ham/sql/query?$IdsFormat=1', data=f'select max(IDT) as max_ID from MESS where CHAT = {chat_id_ham}')
        try:  # Обработка ошибки, если чат создан, но в нем еще нет сообщений
            max_id = json.loads(response.text)['value'][0]['max_id']
        except Exception as inst:
            max_id = -1
    except Exception as inst:
        max_id = -1 
    return max_id

# Переводит дату с одного формата в другой для сохранения Media
def date_reworker(date):
    date = str(date).replace(":", "-")
    return date

# Загружает информацию о чате в БД, возвращает Hameleon'овский id чата
def post_chat_info(chat_id):
    message = next(app.get_chat_history(chat_id, limit=1))
    try:
        data_chat = [{
            "idt": message.chat.id,
            "type": str(message.chat.type),
            "title": message.chat.title,
            "username": message.chat.username,
            "photo_small_file_id": message.chat.photo.small_file_id,
            "small_photo_unique_id": message.chat.photo.small_photo_unique_id
        }]
    except Exception as inst:
        data_chat = [{
            "idt": message.chat.id,
            "type": str(message.chat.type),
            "title": message.chat.title,
            "username": message.chat.username
        }]

    response = requests.post(f'{url}/ham/odata/Chat', json=data_chat)
    chat_id_ham = json.loads(response.text)['NewIDs'][0]
    return chat_id_ham

# Загрузка сообщений в БД
def post_message_info(chat_id, offset_id, chat_id_ham, last_message_id, data_message, count_message_in_db):        
    print(f"[INFO] Перебор сообщений  chat_id = ", chat_id)
    print(f"                          offset_id = ", offset_id)
    print(f"                          last_message_id = ", last_message_id)
    for message in app.get_chat_history(chat_id=chat_id, offset_id=offset_id):
        count = len(data_message)

        # Если мы вдруг дошли до миграции в другой чат, то переключаемся на этот чат
        if message.migrate_from_chat_id:
            # Загружаем сообщения в БД, которые накопились до миграции
            print(f">>>")
            print(f"[INFO] Загрузка последних {len(data_message)+1} сообщений в БД. Миграция в другой чат")
            response = requests.post(f'{url}/ham/odata/', json=data_message)
            print(f"[INFO] Статус загрузки этой части сообщений в БД - {response.status_code}")  
            if response.status_code == 400:
                break 

            # Узнаем ham_id текущего чата (ОТКУДА происходит миграция)
            response = requests.get(f'{url}/ham/sql/query?$IdsFormat=1', data=f'select id from CHAT where idt = {chat_id}')
            chat_id_ham = json.loads(response.text)['value'][0]['$id']

            # Обновляем id чата
            chat_id = message.migrate_from_chat_id  # id чата

            # Сохраняем информацию о миграции (Записываем id чата, КУДА происходит миграция)
            data_chat = [{
                "$id": chat_id_ham,
                "$type": "Chat",
                "migrate_from_chat" : chat_id  
            }]
            response = requests.patch('http://localhost:4388/ham/odata', json=data_chat)

            # Переключаемся на новый чат
            post_info(chat_id=chat_id, offset_id=0)
            data_message = []
            break

        # Сработает для дозагрузки новых сообщений. Если мы дошли до сообщения, которое было последним из БД (last_message_id), 
        # то это значит, что мы прошли по всем новым сообщениям в чате
        if message.id <= last_message_id:
            print(f"[INFO] Было добавлено новых сообщений: {len(data_message)}") 
            break

        # Обрабатываем сообщения, копим их в массиве (data_message), потом записываем в БД
        ausername = ""
        if message.from_user:    
            if message.from_user.first_name:  
                ausername = message.from_user.first_name            
            if message.from_user.last_name:    
                ausername = ausername + " " + message.from_user.last_name 
            if message.from_user.username:    
                ausername = ausername + " " + message.from_user.username
        ausername = ausername.strip()

        if message.mentioned == None:
            try:
                data_message += [{
                        "idt": message.id,
                        "from_user_id": message.from_user.id,
                        "from_user_username": ausername,
                        "date_mes": str(message.date),
                        "forward_from_id": message.forward_from.id if message.forward_from else None,
                        "forward_from_username": message.forward_from.username if message.forward_from else None,
                        "forward_date": str(message.forward_date) if message.forward_date else None,
                        "reply_to_message_id": message.reply_to_message_id if message.reply_to_message_id else None,
                        "mentioned": "True" if message.mentioned else "False",
                        "scheduled": "True" if message.scheduled else "False",
                        "from_scheduled": "True" if message.from_scheduled else "False",
                        "has_protected_content": "True" if message.has_protected_content else "False",
                        "text": message.text if message.text else None,
                        "outgoing": "True" if message.outgoing else "False",
                        "unknown_message": str(message),
                        "Chat@ref": f'Chat({chat_id_ham})',
                        "$type": "Message"
                    }]
            except Exception as inst:
                data_message += [{
                    "idt": message.id,
                    "date_mes": str(message.date),                
                    "unknown_message": str(message),
                    "Chat@ref": f'Chat({chat_id_ham})',
                    "$type": "Message"
                }]
        else:
            atext = message.text if message.text else None
            if message.caption:
                atext = message.caption if message.caption else atext
                
            try:
                data_message += [{
                    "idt": message.id,
                    "from_user_id": message.from_user.id,
                    "from_user_username": ausername,
                    "date_mes": str(message.date),
                    "forward_from_id": message.forward_from.id if message.forward_from else None,
                    "forward_from_username": message.forward_from.username if message.forward_from else None,
                    "forward_date": str(message.forward_date) if message.forward_date else None,
                    "reply_to_message_id": message.reply_to_message_id if message.reply_to_message_id else None,
                    "mentioned": "True" if message.mentioned else "False",
                    "scheduled": "True" if message.scheduled else "False",
                    "from_scheduled": "True" if message.from_scheduled else "False",
                    "has_protected_content": "True" if message.has_protected_content else "False",
                    "text": atext,
                    "unknown_message": str(message),  # Debug    
                    "outgoing": "True" if message.outgoing else "False",
                    "Chat@ref": f'Chat({chat_id_ham})'
                }]
            except Exception as inst:
                data_message += [{
                    "idt": message.id,
                    "date_mes": str(message.date),                
                    "unknown_message": str(message),
                    "Chat@ref": f'Chat({chat_id_ham})',
                    "$type": "Message"
                }]
            if message.photo:
                if not os.path.isfile(f"Media\{chat_id}\{date_reworker(message.date)}_{message.id}.jpg"):
                    app.download_media(message.photo.file_id, file_name=f"Media\{chat_id}\{date_reworker(message.date)}_{message.id}.jpg")
                data_message[count].update({
                    "$type": "Photo",
                    "file_id": message.photo.file_id,
                    "file_size": message.photo.file_size,
                    "date_photo": str(message.photo.date),
                    "caption": message.caption if message.caption else None,
                    "path": str(f"Media\{chat_id}\{date_reworker(message.date)}_{message.id}.jpg")
                })
            elif message.video:
                if not os.path.isfile(f"Media/{chat_id}/{date_reworker(message.date)}_{message.id}.mp4"):
                    app.download_media(message.video.file_id, file_name=f"Media\{chat_id}\{date_reworker(message.date)}_{message.id}.mp4")
                data_message[count].update({
                    "$type": "Video",
                    "file_id": message.video.file_id,
                    "file_size": message.video.file_size,
                    "mime_type": message.video.mime_type,
                    "duration": message.video.duration,
                    "date_video": str(message.video.date),
                    "caption": message.caption if message.caption else None,
                    "path": str(f"Media\{chat_id}\{date_reworker(message.date)}_{message.id}.mp4")
                })
            elif message.voice:
                if not os.path.isfile(f"Media/{chat_id}/{date_reworker(message.date)}_{message.id}.ogg"):
                    app.download_media(message.voice.file_id, file_name=f"Media\{chat_id}\{date_reworker(message.date)}_{message.id}.ogg")    
                data_message[count].update({
                    "$type": "Voice",
                    "file_id": message.voice.file_id,
                    "file_size": message.voice.file_size,
                    "mime_type": message.voice.mime_type,
                    "duration": message.voice.duration,
                    "date_voice": str(message.voice.date),
                    "path": str(f"Media\{chat_id}\{date_reworker(message.date)}_{message.id}.ogg")
                })
            elif message.sticker:
                if not os.path.isfile(f"Media/{chat_id}/{date_reworker(message.date)}_{message.id}.jpg"):
                    app.download_media(message.sticker.file_id, file_name=f"Media/{chat_id}/{date_reworker(message.date)}_{message.id}.jpg")    
                data_message[count].update({
                    "$type": "Sticker",
                    "file_id": message.sticker.file_id,
                    "file_size": message.sticker.file_size,
                    "mime_type": message.sticker.mime_type,
                    "date_sticker": str(message.sticker.date),
                    "emoji": message.sticker.emoji,
                    "set_name": message.sticker.set_name,
                    "path": str(f"Media\{chat_id}\{date_reworker(message.date)}_{message.id}.jpg")
                })
            else:
                data_message[count].update({"$type": "Message"})

        # Условие загрузки сообщений в БД пачками по 100 штук сообщений
        if len(data_message)+1 == bulk_count:
            count_message_in_db += bulk_count
            print(f">>>")
            print(f"[INFO] Загрузка {bulk_count} сообщений в БД. Всего загружено {count_message_in_db} сообщений")
            response = requests.post(f'{url}/ham/odata/', json=data_message)
            data_message = []
            print(f"[INFO] Статус загрузки этой части сообщений в БД - {response.status_code}")    
            if response.status_code == 400:
                break   
    
    # Условие загрузки сообщений в БД пачкой, когда в ней меньше 100 штук сообщений (По сути - самые последние сообщения)
    if len(data_message)+1 < bulk_count and len(data_message) != 0:
        count_message_in_db += bulk_count
        print(f">>>")
        print(f"[INFO] Загрузка последних {len(data_message)+1} сообщений в БД. Всего загружено {count_message_in_db} сообщений")
        response = requests.post(f'{url}/ham/odata/', json=data_message)
        print(f"[INFO] Статус загрузки этой части сообщений в БД - {response.status_code}")




def post_info(chat_id, offset_id):
    # Проверка на наличие записи о чате в БД, в итоге получим ham_id чата / id последнего сообщения
    print(f"[INFO] Проверка на наличие чата в БД")
    response = requests.get(f'{url}/ham/sql/query?$IdsFormat=1', data=f'select id from CHAT where idt = {chat_id}')
    try:
        # Проверка на наличие записи о чате в БД (Пытаемся получить ham_id)
        chat_id_ham = json.loads(response.text)['value'][0]['$id']

        # Проврека на существование миграций.
        response = requests.get(f'{url}/ham/sql/query?$IdsFormat=1', data=f'select migrate_from_chat from CHAT where idt = {chat_id}')
        migrate_to_chat = json.loads(response.text)['value'][0]['migrate_from_chat']
        if migrate_to_chat != None: 
            print(f"[INFO] Обнаружена миграция, переключаемся на другой чат")
            # Миграция есть - сразу перескакиваем на следующий чат
            chat_id = migrate_to_chat
            offset_id = min_id(migrate_to_chat)
            post_info(chat_id=chat_id, offset_id=offset_id)
        else:
            # Миграций нет - начинаем парсить сообщений
            if offset_id == 0:
                last_message_id = max_id()
                print(f"[INFO] Чат найден, начинаю загрузку новых сообщений")
            else:
                last_message_id = -1
                print(f"[INFO] Чат найден, начинаю загрузку полной истории сообщений")

            # Загрузка сообщений в БД
            post_message_info(chat_id, offset_id, chat_id_ham, last_message_id, data_message=[], count_message_in_db=0)
    except Exception as inst:
        chat_id_ham = post_chat_info(chat_id)
        last_message_id = -1
        print(f"[INFO] Информация о новом чате записана, начинаю загрузку полной истории сообщений")
    
        # Загрузка сообщений в БД
        post_message_info(chat_id, offset_id, chat_id_ham, last_message_id, data_message=[], count_message_in_db=0)
    

# Определяем параметры - id чата / id сообщения, с которого начинаем парсинг
count_param = len(sys.argv) - 1
if count_param == 0:
    chat_id = "KOJIEHO"
    offset_id = 0
if count_param == 1:
    chat_id = sys.argv[1]
    offset_id = 0
if count_param == 2:
    chat_id = sys.argv[1]
    offset_id = min_id(chat_id)
    

with Client(name="my_account", api_hash=api_hash, api_id=api_id) as app:
    post_info(chat_id=chat_id, offset_id=offset_id)

import sys
sys.path.append("PLIB")

from pyrogram import Client
import configparser
import json
import requests
import os.path


config = configparser.ConfigParser()
config.read("settings.ini")

url = config["CONFIG"]["url"]
bulk_count = int(config["CONFIG"]["bulk_count"])


# Поиск минимального id сообщения в БД
def min_id():
    response = requests.get(f'{url}/ham/odata/Chat')
    chats = json.loads(response.text)['value']
    min_id = 0
    if len(chats) == 0:
        min_id = 0
    else:
        for count, chat in enumerate(chats):
            if chat['username'] == chat_id or str(chat['idt']) == chat_id:
                response = requests.get(f'{url}/ham/odata/Message')
                messages = json.loads(response.text)['value']
                
                for message in messages:
                    if message["Chat@ref"] == chat['Message@list'].split("/")[0]:
                        min_id = message["idt"]
                        break
                for message in messages:
                    if message["Chat@ref"] == chat['Message@list'].split("/")[0]:
                        if min_id > message["idt"]:
                            min_id = message["idt"]
                break
            
            if count + 1 == len(chats):
                min_id = 0
    return min_id

# Переводит дату с одного формата в другой для сохранения Media
def date_reworker(date):
    date = str(date).replace(":", "-")
    return date

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
    offset_id = min_id()

chat_id = "urik_terkin"
offset_id = 0

# Сохранение истории сообщений
def post_info():
    # Загружает информацию о чате в БД, возвращает Hameleon'овский id чата
    def post_chat_info():
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

            if message.migrate_from_chat_id:
                post_message_info(chat_id=message.migrate_from_chat_id, offset_id=0, chat_id_ham=chat_id_ham, last_message_id=last_message_id, data_message=data_message, count_message_in_db=count_message_in_db)
                data_message = []
                break
            
            if message.id <= last_message_id:
                print(f"[INFO] Было добавлено новых сообщений: {len(data_message)}") 
                break


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


    # Проверка на наличие записи о чате в БД, в итоге получим ham_id чата / id последнего сообщения
    print(f"[INFO] Проверка на наличие чата в БД")
    response = requests.get(f'{url}/ham/odata/Chat')
    chats = json.loads(response.text)['value']
    if len(chats) == 0:
        chat_id_ham = post_chat_info()
        last_message_id = -1
        print(f"[INFO] Информация о новом чате записана, начинаю загрузку истории сообщений")
    else:
        for count, chat in enumerate(chats):
            if chat['username'] == chat_id or str(chat['idt']) == chat_id:
                chat_id_ham = chat['$id']
                if offset_id == 0:
                    response = requests.get(f'{url}/ham/odata/Message')
                    messages = json.loads(response.text)['value']
                    max_id = 0
                    for message in messages:
                        if message["Chat@ref"] == chat['Message@list'].split("/")[0]:
                            if max_id < message["idt"]:
                                max_id = message["idt"]
                    last_message_id = max_id
                    print(f"[INFO] Чат найден, начинаю загрузку новых сообщений")
                else:
                    last_message_id = -1
                print(f"[INFO] Чат найден, начинаю загрузку истории сообщений")
                break
            if count + 1 == len(chats):
                chat_id_ham = post_chat_info()
                last_message_id = -1
                print(f"[INFO] Информация о новом чате записана, начинаю загрузку истории сообщений")
        
    # Загрузка истории сообщений в БД
    post_message_info(chat_id, offset_id, chat_id_ham, last_message_id, data_message=[], count_message_in_db=0)
    
    
api_hash = config["CONFIG"]["api_hash"]
api_id = config["CONFIG"]["api_id"]

with Client(name="my_account", api_hash=api_hash, api_id=api_id) as app:
    post_info()

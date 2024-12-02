from pyrogram import Client
import configparser
import sys
sys.path.append("PLIB")


config = configparser.ConfigParser()
config.read("settings.ini")

api_hash = config["CONFIG"]["api_hash"]
api_id = config["CONFIG"]["api_id"]


with Client(name="my_account", api_hash=api_hash, api_id=api_id) as app:
    count = 1
    file = open('chats_list.txt', 'w', encoding="utf-8")
    for dialog in app.get_dialogs():
        chat_info = dialog.chat
        file.write(f"{count}. {chat_info.id}      {chat_info.title if chat_info.title else chat_info.first_name}      {chat_info.type}\n")
        print(f"{count}. {chat_info.id}      {chat_info.title if chat_info.title else chat_info.first_name}      {chat_info.type}\n")
    file.close()

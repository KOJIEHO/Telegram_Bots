from pyrogram import Client
import configparser
import json
import requests
import os.path
import sys
from datetime import datetime, timedelta

sys.path.append("PLIB")
config = configparser.ConfigParser()
config.read("settings.ini")

api_hash = config["CONFIG"]["api_hash"]
api_id = config["CONFIG"]["api_id"]
url = config["CONFIG"]["url"]
bulk_count = int(config["CONFIG"]["bulk_count"])
    

with Client(name="my_account", api_hash=api_hash, api_id=api_id) as app:
    for message in app.get_chat_history(chat_id=948112673, offset_id=0):
        # Пример времени из Pyrogram (UTC)
        utc_time = message.date
        print(utc_time)

        # Твой часовой пояс (например, +3 часа)
        local_time = utc_time + timedelta(hours=3)
        print(local_time)

        break

    

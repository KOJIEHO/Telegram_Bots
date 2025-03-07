import sys
sys.path.append("PLIB")

from pyrogram import Client
import configparser
import json
import requests
import os.path


# config = configparser.ConfigParser()
# config.read("settings.ini")

# url = config["CONFIG"]["url"]
# bulk_count = int(config["CONFIG"]["bulk_count"])

    
# api_hash = config["CONFIG"]["api_hash"]
# api_id = config["CONFIG"]["api_id"]

# with Client(name="my_account", api_hash=api_hash, api_id=api_id) as app:
#     count = 0
#     for message in app.get_chat_history(chat_id="poligoonn", offset_id=0):
#         count += 1
#         print(message)
#         if count == 2:
#             break

# fetch('http://localhost:4388/ham/sql/query?$IdsFormat=1', {
#                         method: 'POST',
#                         headers: { 'Content-Type': 'text/plain' },
#                         body: ``
#                     })

# response = requests.get('http://localhost:4388/ham/sql/query?$IdsFormat=1', data='select min(IDT) as min_ID,  max(IDT) as max_ID from MESS where CHAT = 1')
# print(json.loads(response.text))

response = requests.get('http://localhost:4388/ham/sql/query?$IdsFormat=1', data='select migrate_from_chat from CHAT where idt = 482250576')
# try:
print(json.loads(response.text)['value'][0]['migrate_from_chat'])
if json.loads(response.text)['value'][0]['migrate_from_chat'] == None:
    print("qwer")
# except Exception as inst:
#     print(json.loads(response.text)['value'])


# data_chat = [{
#     "$id": 66,
#     "$type": "Chat",
#     "migrate_from_chat" : 123
# }]

# response = requests.get('http://localhost:4388/ham/odata/Chat', json=data_chat)
# print(json.loads(response.text))
# chat_id_ham = json.loads(response.text)['NewIDs'][0]
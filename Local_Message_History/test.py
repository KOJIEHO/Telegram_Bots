# import requests

# 1) odata+sql
# url = f'http://localhost:4388/ham/odata/$sql'
# body = 'select id, type_id from MESSAGE where CHAT = 1 order by DATE_MES desc, ID desc'
# # body = 'select id, type_id ' + \
# # 'from MESSAGE ' + \
# # 'where CHAT = 1 ' + \
# # 'order by DATE_MES desc, ID desc'

# # " 
# # select ID, TYPE_ID
# #  from MESSAGE
# #  where CHAT = 1
# #  order by DATE_MES  desc , ID desc"
# # print(body)
# headers = {
#     'Content-Type': 'text/plain'
# }
# response = requests.get(url=url, data=body, headers=headers)
# print(response)

# 2) sql
# url = f'http://localhost:4388/ham/sql/query?$IdsFormat=0'
# body = 'select * from MESSAGE where CHAT = 1 order by DATE_MES desc, ID desc'
# # print(body)
# response = requests.post(url=url, data=body)
# print(response.text)
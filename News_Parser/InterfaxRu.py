import requests
from bs4 import BeautifulSoup
from universal_DB_connection import DB_maker

URL_InterfaxRu1 = 'https://www.interfax.ru/business/'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}

# Ссылки
##################################################################################################
def get_links_InterfaxRu():
    global link_InterfaxRu

    response = requests.get(URL_InterfaxRu1, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    link_InterfaxRu = [
        a.get('href')
        for a in soup.find_all('a')
        if a.get('href') and a.get('href').startswith('/business/')
    ]
    link_InterfaxRu = link_InterfaxRu[1:2]
    link_InterfaxRu[0] = 'https://www.interfax.ru/' + link_InterfaxRu[0]

    return link_InterfaxRu
##################################################################################################

# Заголовки
##################################################################################################
def get_headers_InterfaxRu():
    global header_InterfaxRu

    response = requests.get(str(link_InterfaxRu[0]), timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    date0 = soup.find("a", {"class": "time"}).text
    date0 = " ".join(date0.split())
    header0 = soup.find("h1").text
    header_InterfaxRu = [date0 + "\n" + header0]

    return header_InterfaxRu
##################################################################################################

# Основная часть
##################################################################################################
def main_InterfaxRu():
    get_links_InterfaxRu()
    get_headers_InterfaxRu()
    DB_maker('InterfaxRu', link_InterfaxRu[0], header_InterfaxRu[0])
##################################################################################################
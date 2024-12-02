import requests
from bs4 import BeautifulSoup
from universal_DB_connection import DB_maker

URL_GazetaRu1 = 'https://www.gazeta.ru/news/'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36",
    "accept": "*/*"}

# Ссылки
##################################################################################################
def get_links_GazetaRu():
    global link_GazetaRu
    response = requests.get(URL_GazetaRu1, timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    link_GazetaRu = [
        a.get('href')
        for a in soup.find_all('a')
        if a.get('href') and a.get('href').startswith('')
    ]
    link_GazetaRu = link_GazetaRu[47:48]
    link_GazetaRu[0] = 'https://www.gazeta.ru' + link_GazetaRu[0]
    return link_GazetaRu
##################################################################################################
# Заголовки
##################################################################################################
def get_headers_GazetaRu():
    global header_GazetaRu
    response = requests.get(str(link_GazetaRu[0]), timeout=30, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    date0 = soup.find("time", {"class": "time"}).text
    date0 = " ".join(date0.split())
    header0 = soup.find("h1").text
    header0 = " ".join(header0.split())
    header_GazetaRu = [date0 + '\n' + header0]
    return header_GazetaRu
##################################################################################################
# Основная часть
##################################################################################################
def main_GazetaRu():
    get_links_GazetaRu()
    get_headers_GazetaRu()
    DB_maker('GazetaRu', link_GazetaRu[0], header_GazetaRu[0])
##################################################################################################
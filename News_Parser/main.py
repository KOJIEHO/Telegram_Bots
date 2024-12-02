import asyncio
import telebot
from user_id import token

from GazetaRu import main_GazetaRu
from InterfaxRu import main_InterfaxRu
from IzRu import main_IzRu

# from LentaRu import main_LentaRu

# from NasdaqCom import main_NasdaqCom
# from OilWorldRu import main_OilWorldRu
# from RbkRu import main_RbkRu
# from RgRu import main_RgRu
# from SpGlobalCom import main_SpGlobalCom
# from ZernoRu import main_ZernoRu
# from ZolRu import main_ZolRu
# from ForbesRu import main_ForbesRu
# from KommersantRu import main_KommersantRu
# from PrimeRu import main_PrimeRu
# from VedomostiRu import main_VedomostiRu
# from AgricultureCom import main_AgricultureCom
# from RiaRu import main_RiaRu

bot = telebot.TeleBot(token)


async def check_news_update():
    while True:
        # try:
            main_GazetaRu() # Тут вроде все ок
            main_InterfaxRu() # Есть смысл переделать на "общие" новости. Пока тут только экономика
            main_IzRu() # Тут вроде все ок

            # main_LentaRu()
            # main_NasdaqCom()
            # main_OilWorldRu()
            # main_RbkRu()
            # main_RgRu()
            # main_SpGlobalCom()
            # main_ZernoRu()
            # main_ZolRu()
            # main_ForbesRu()
            # main_KommersantRu()
            # main_PrimeRu()
            # main_VedomostiRu()
            # main_AgricultureCom()
            # main_RiaRu()
            # print('##################################################################################################')
            await asyncio.sleep(60)
        # except Exception:
        #     # continue
        #     print(Exception)
        #     print('Сломался')


if __name__ == '__main__':
    asyncio.run(check_news_update())
    bot.polling(none_stop=True)

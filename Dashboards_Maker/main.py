from aiogram import Bot, types
from PIL import Image, ImageDraw, ImageFont
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import csv
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


token = ''
bot = Bot(token=token)
db = Dispatcher(bot)


@db.message_handler()
async def textnew(message: types.Message):
    id = message.chat.id
    message_arr = message.text.split()

    # Внутренний Рынок
    if str(message_arr[0]) == 'Рынок':
        base = sqlite3.connect('db/PhotoRinok.db')
        cur = base.cursor()
        image = Image.open("png/ВнутреннийРынокФон.png")
        idraw = ImageDraw.Draw(image)

        font = ImageFont.truetype("ttf/articulat-cf-extra-light.ttf", size=35)
        idraw.text((800, 310), message_arr[1], font=font)

        font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=20)
        PosX = 522
        PosX1 = 707
        PosY = 673
        count_db_table = 1
        count = 2
        while count < 20:
            info0 = cur.execute('SELECT info0 FROM line' + str(count_db_table)).fetchall()
            info1 = cur.execute('SELECT info1 FROM line' + str(count_db_table)).fetchall()
            if str(message_arr[count]) == '-':
                idraw.text((PosX+22, PosY-10), '_', font=font, fill="#a8a8a6")  # 1 0
                idraw.text((PosX+27, PosY-10), '_', font=font, fill="#a8a8a6")  # Для жирности
            elif str(info0[0][0]) == '-':
                message_arr_output = message_arr[count][:len(message_arr[count]) - 3] + ' ' + message_arr[count][len(message_arr[count]) - 3:len(message_arr[count])]
                idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6", radius=7)
                idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0
            else:
                if int(info0[0][0]) == int(message_arr[count]):
                    message_arr_output = message_arr[count][:len(message_arr[count]) - 3] + ' ' + message_arr[count][len(message_arr[count]) - 3:len(message_arr[count])]
                    idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6", radius=7)
                    idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0
                elif int(info0[0][0]) < int(message_arr[count]):
                    if str(info0[0][0]) != '-':
                        message_arr_output = message_arr[count][:len(message_arr[count]) - 3] + ' ' + message_arr[count][len(message_arr[count]) - 3:len(message_arr[count])]
                        idraw.rounded_rectangle((PosX - 7, PosY - 15 - 7, PosX - 7 + 80, PosY - 15 - 7 + 31), fill="#67a947", radius=7)
                        idraw.text((PosX, PosY - 15), message_arr_output, font=font, fill='#ffffff')  # 1 0
                        idraw.text((PosX+1, PosY-15), message_arr_output, font=font, fill='#ffffff')  # Для жирности
                        info0output = info0[0][0][:len(info0[0][0]) - 3] + ' ' + info0[0][0][len(info0[0][0]) - 3:len(info0[0][0])]
                        idraw.text((PosX+5, PosY + 15), info0output, font=font, fill='#ffffff')  # 1 0
                    else:
                        message_arr_output = message_arr[count][:len(message_arr[count]) - 3] + ' ' + message_arr[count][len(message_arr[count]) - 3:len(message_arr[count])]
                        idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6", radius=7)
                        idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0
                elif int(info0[0][0]) > int(message_arr[count]):
                    if str(info0[0][0]) != '-':
                        message_arr_output = message_arr[count][:len(message_arr[count]) - 3] + ' ' + message_arr[count][len(message_arr[count]) - 3:len(message_arr[count])]
                        idraw.rounded_rectangle((PosX - 7, PosY - 15 - 7, PosX - 7 + 80, PosY - 15 - 7 + 31), fill="#ac4540", radius=7)
                        idraw.text((PosX, PosY - 15), message_arr_output, font=font, fill='#ffffff')  # 1 0
                        idraw.text((PosX+1, PosY-15), message_arr_output, font=font, fill='#ffffff')  # Для жирности
                        info0output = info0[0][0][:len(info0[0][0]) - 3] + ' ' + info0[0][0][len(info0[0][0]) - 3:len(info0[0][0])]
                        idraw.text((PosX+5, PosY + 15), info0output, font=font, fill='#ffffff')  # 1 0
                    else:
                        message_arr_output = message_arr[count][:len(message_arr[count]) - 3] + ' ' + message_arr[count][len(message_arr[count]) - 3:len(message_arr[count])]
                        idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6", radius=7)
                        idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0

            if str(message_arr[count+1]) == '-':
                idraw.text((PosX1+22, PosY-10), '_', font=font, fill="#a8a8a6")  # 0 1
                idraw.text((PosX1+27, PosY-10), '_', font=font, fill="#a8a8a6")  # Для жирности
            elif str(info1[0][0]) == '-':
                message_arr_output = message_arr[count + 1][:len(message_arr[count + 1]) - 3] + ' ' + message_arr[count + 1][len(message_arr[count + 1]) - 3:len(message_arr[count + 1])]
                idraw.rounded_rectangle((PosX1 - 7, PosY - 7, PosX1 - 7 + 80, PosY - 7 + 31), fill="#a8a8a6", radius=7)
                idraw.text((PosX1, PosY), message_arr_output, font=font, fill='black')  # 0 1
            else:
                if int(info1[0][0]) == int(message_arr[count + 1]):
                    message_arr_output = message_arr[count+1][:len(message_arr[count+1]) - 3] + ' ' + message_arr[count+1][len(message_arr[count+1]) - 3:len(message_arr[count+1])]
                    idraw.rounded_rectangle((PosX1 - 7, PosY - 7, PosX1 - 7 + 80, PosY - 7 + 31), fill="#a8a8a6", radius=7)
                    idraw.text((PosX1, PosY), message_arr_output, font=font, fill='black')  # 0 1
                elif int(info1[0][0]) < int(message_arr[count + 1]):
                    if str(info1[0][0]) != '-':
                        message_arr_output = message_arr[count+1][:len(message_arr[count+1]) - 3] + ' ' + message_arr[count+1][len(message_arr[count+1]) - 3:len(message_arr[count+1])]
                        idraw.rounded_rectangle((PosX1 - 7, PosY - 15 - 7, PosX1 - 7 + 80, PosY - 15 - 7 + 31), fill="#67a947", radius=7)
                        idraw.text((PosX1, PosY - 15), message_arr_output, font=font, fill='#ffffff')  # 1 0
                        idraw.text((PosX1+1, PosY-15), message_arr_output, font=font, fill='#ffffff')  # Для жирности
                        info1output = info1[0][0][:len(info1[0][0]) - 3] + ' ' + info1[0][0][len(info1[0][0]) - 3:len(info1[0][0])]
                        idraw.text((PosX1+5, PosY + 15), info1output, font=font, fill='#ffffff')  # 1 0
                    else:
                        message_arr_output = message_arr[count+1][:len(message_arr[count+1]) - 3] + ' ' + message_arr[count+1][len(message_arr[count+1]) - 3:len(message_arr[count+1])]
                        idraw.rounded_rectangle((PosX1 - 7, PosY - 7, PosX1 - 7 + 80, PosY - 7 + 31), fill="#a8a8a6", radius=7)
                        idraw.text((PosX1, PosY), message_arr_output, font=font, fill='black')  # 0 1
                elif int(info1[0][0]) > int(message_arr[count + 1]):
                    if str(info1[0][0]) != '-':
                        message_arr_output = message_arr[count+1][:len(message_arr[count+1]) - 3] + ' ' + message_arr[count+1][len(message_arr[count+1]) - 3:len(message_arr[count+1])]
                        idraw.rounded_rectangle((PosX1 - 7, PosY - 15 - 7, PosX1 - 7 + 80, PosY - 15 - 7 + 31), fill="#ac4540", radius=7)
                        idraw.text((PosX1, PosY - 15), message_arr_output, font=font, fill='#ffffff')  # 1 0
                        idraw.text((PosX1+1, PosY-15), message_arr_output, font=font, fill='#ffffff')  # Для жирности
                        info1output = info1[0][0][:len(info1[0][0]) - 3] + ' ' + info1[0][0][len(info1[0][0]) - 3:len(info1[0][0])]
                        idraw.text((PosX1+5, PosY + 15), info1output, font=font, fill='#ffffff')  # 1 0
                    else:
                        message_arr_output = message_arr[count+1][:len(message_arr[count+1]) - 3] + ' ' + message_arr[count+1][len(message_arr[count+1]) - 3:len(message_arr[count+1])]
                        idraw.rounded_rectangle((PosX1 - 7, PosY - 7, PosX1 - 7 + 80, PosY - 7 + 31), fill="#a8a8a6", radius=7)
                        idraw.text((PosX1, PosY), message_arr_output, font=font, fill='black')  # 0 1
            if count_db_table == 1 or count_db_table == 4 or count_db_table == 6:
                PosY += 80
            if count_db_table == 2 or count_db_table == 3 or count_db_table == 5 or count_db_table == 7 or count_db_table == 8:
                PosY += 85

            cur.execute('DROP TABLE line' + str(count_db_table))
            base.commit()
            base.execute('CREATE TABLE IF NOT EXISTS line' + str(count_db_table) + '(info0, info1)')
            base.commit()
            cur.execute('INSERT INTO line' + str(count_db_table) + ' VALUES(?, ?)', (message_arr[count], message_arr[count + 1]))
            base.commit()
            base.execute('CREATE TABLE IF NOT EXISTS DBlinePlot' + str(count_db_table) + '(date, info0, info1)')
            base.commit()
            cur.execute('INSERT INTO DBlinePlot' + str(count_db_table) + ' VALUES(?, ?, ?)', (message_arr[1], message_arr[count], message_arr[count + 1]))
            base.commit()
            count_db_table += 1
            count += 2
        image = image.crop((60, 0, 1020, 1420))
        image.save('png/ВнутреннийРынокИтог.png')
        image0 = open('png/ВнутреннийРынокИтог.png', 'rb')
        await bot.send_photo(id, image0)

    # Экспорт
    count = 0
    while count < 1:
        count += 1
        if str(message_arr[0]) == 'Экспорт':
            base = sqlite3.connect('db/PhotoEksport.db')
            cur = base.cursor()
            image = Image.open("png/ЭкспортФон.png")
            idraw = ImageDraw.Draw(image)

            font = ImageFont.truetype("ttf/articulat-cf-extra-light.ttf", size=38)
            idraw.text((791, 310), message_arr[1], font=font)

            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=20)
            PosX = 497
            PosY = 685
            count_db_table = 1
            count = 2
            while count < 16:
                info0 = cur.execute('SELECT info0 FROM line' + str(count_db_table)).fetchall()
                info1 = cur.execute('SELECT info1 FROM line' + str(count_db_table)).fetchall()
                info2 = cur.execute('SELECT info2 FROM line' + str(count_db_table)).fetchall()
                info3 = cur.execute('SELECT info3 FROM line' + str(count_db_table)).fetchall()
                if str(message_arr[count]) == '-':
                    idraw.text((PosX + 22, PosY - 10), '_', font=font, fill="#a8a8a6")  # 1 0 0 0
                    idraw.text((PosX + 27, PosY - 10), '_', font=font, fill="#a8a8a6")  # Для жирности
                elif str(info0[0][0]) == '-':
                    if message_arr[count].find('/') == -1:
                        message_arr_output = message_arr[count][:len(message_arr[count]) - 3] + ' ' + message_arr[
                                                                                                          count][len(
                            message_arr[count]) - 3:len(message_arr[count])]
                        idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6",
                                                radius=7)
                        idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0 0 0
                    else:
                        number_one = message_arr[count][:message_arr[count].find('/')]
                        number_two = message_arr[count][message_arr[count].find('/') + 1:]
                        message_arr_output0 = number_one[:len(number_one) - 3] + ' ' + number_one[
                                                                                       len(number_one) - 3:len(
                                                                                           number_one)]
                        message_arr_output1 = number_two[:len(number_two) - 3] + ' ' + number_two[
                                                                                       len(number_two) - 3:len(
                                                                                           number_two)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.rounded_rectangle((PosX - 7 - 35, PosY - 7, PosX - 7 + 80 + 35, PosY - 7 + 31),
                                                fill="#a8a8a6", radius=7)
                        idraw.text((PosX - 35, PosY), message_arr_output, font=font, fill='black')
                elif message_arr[count].find('/') > 0:
                    number_one0 = info0[0][0][:info0[0][0].find('/')]
                    number_two0 = info0[0][0][info0[0][0].find('/') + 1:]
                    number_one = message_arr[count][:message_arr[count].find('/')]
                    number_two = message_arr[count][message_arr[count].find('/') + 1:]
                    if int(number_one0) == int(number_one):
                        message_arr_output0 = number_one[:len(number_one) - 3] + ' ' + number_one[
                                                                                       len(number_one) - 3:len(
                                                                                           number_one)]
                        message_arr_output1 = number_two[:len(number_two) - 3] + ' ' + number_two[
                                                                                       len(number_two) - 3:len(
                                                                                           number_two)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.rounded_rectangle((PosX - 7 - 35, PosY - 7, PosX - 7 + 80 + 35, PosY - 7 + 31),
                                                fill="#a8a8a6", radius=7)
                        idraw.text((PosX - 35, PosY), message_arr_output, font=font, fill='black')
                    elif int(number_one0) < int(number_one):
                        message_arr_output0 = number_one[:len(number_one) - 3] + ' ' + number_one[
                                                                                       len(number_one) - 3:len(
                                                                                           number_one)]
                        message_arr_output1 = number_two[:len(number_two) - 3] + ' ' + number_two[
                                                                                       len(number_two) - 3:len(
                                                                                           number_two)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.rounded_rectangle((PosX - 7 - 35, PosY - 7 - 10, PosX - 7 + 80 + 35, PosY - 7 + 31 - 10),
                                                fill="#67a947", radius=7)
                        idraw.text((PosX - 35, PosY - 10), message_arr_output, font=font, fill='#ffffff')
                        message_arr_output0 = number_one0[:len(number_one0) - 3] + ' ' + number_one0[
                                                                                         len(number_one0) - 3:len(
                                                                                             number_one0)]
                        message_arr_output1 = number_two0[:len(number_two0) - 3] + ' ' + number_two0[
                                                                                         len(number_two0) - 3:len(
                                                                                             number_two0)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.text((PosX - 35, PosY + 17), message_arr_output, font=font, fill='#ffffff')

                    elif int(number_one0) > int(number_one):
                        message_arr_output0 = number_one[:len(number_one) - 3] + ' ' + number_one[
                                                                                       len(number_one) - 3:len(
                                                                                           number_one)]
                        message_arr_output1 = number_two[:len(number_two) - 3] + ' ' + number_two[
                                                                                       len(number_two) - 3:len(
                                                                                           number_two)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.rounded_rectangle((PosX - 7 - 35, PosY - 7 - 10, PosX - 7 + 80 + 35, PosY - 7 + 31 - 10),
                                                fill="#ac4540", radius=7)
                        idraw.text((PosX - 35, PosY - 10), message_arr_output, font=font, fill='#ffffff')
                        message_arr_output0 = number_one0[:len(number_one0) - 3] + ' ' + number_one0[
                                                                                         len(number_one0) - 3:len(
                                                                                             number_one0)]
                        message_arr_output1 = number_two0[:len(number_two0) - 3] + ' ' + number_two0[
                                                                                         len(number_two0) - 3:len(
                                                                                             number_two0)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.text((PosX - 35, PosY + 17), message_arr_output, font=font, fill='#ffffff')
                else:
                    if int(info0[0][0]) == int(message_arr[count]):
                        message_arr_output = message_arr[count][:len(message_arr[count]) - 3] + ' ' + message_arr[
                                                                                                          count][len(
                            message_arr[count]) - 3:len(message_arr[count])]
                        idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6",
                                                radius=7)
                        idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0 0 0
                    elif int(info0[0][0]) < int(message_arr[count]):
                        if str(info0[0][0]) != '-':
                            message_arr_output = message_arr[count][:len(message_arr[count]) - 3] + ' ' + message_arr[
                                                                                                              count][
                                                                                                          len(
                                                                                                              message_arr[
                                                                                                                  count]) - 3:len(
                                                                                                              message_arr[
                                                                                                                  count])]
                            idraw.rounded_rectangle((PosX - 7, PosY - 12 - 7, PosX - 7 + 80, PosY - 12 - 7 + 31),
                                                    fill="#67a947", radius=7)
                            idraw.text((PosX, PosY - 12), message_arr_output, font=font, fill='#ffffff')  # 1 0 0 0
                            idraw.text((PosX + 1, PosY - 12), message_arr_output, font=font,
                                       fill='#ffffff')  # Для жирности
                            info0output = info0[0][0][:len(info0[0][0]) - 3] + ' ' + info0[0][0][
                                                                                     len(info0[0][0]) - 3:len(
                                                                                         info0[0][0])]
                            idraw.text((PosX, PosY + 18), info0output, font=font, fill='#ffffff')  # 1 0 0 0
                        else:
                            message_arr_output = message_arr[count][:len(message_arr[count]) - 3] + ' ' + message_arr[
                                                                                                              count][
                                                                                                          len(
                                                                                                              message_arr[
                                                                                                                  count]) - 3:len(
                                                                                                              message_arr[
                                                                                                                  count])]
                            idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6",
                                                    radius=7)
                            idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0 0 0
                    elif int(info0[0][0]) > int(message_arr[count]):
                        if str(info0[0][0]) != '-':
                            message_arr_output = message_arr[count][:len(message_arr[count]) - 3] + ' ' + message_arr[
                                                                                                              count][
                                                                                                          len(
                                                                                                              message_arr[
                                                                                                                  count]) - 3:len(
                                                                                                              message_arr[
                                                                                                                  count])]
                            idraw.rounded_rectangle((PosX - 7, PosY - 12 - 7, PosX - 7 + 80, PosY - 12 - 7 + 31),
                                                    fill="#ac4540", radius=7)
                            idraw.text((PosX, PosY - 12), message_arr_output, font=font, fill='#ffffff')  # 1 0 0 0
                            idraw.text((PosX + 1, PosY - 12), message_arr_output, font=font,
                                       fill='#ffffff')  # Для жирности
                            info0output = info0[0][0][:len(info0[0][0]) - 3] + ' ' + info0[0][0][
                                                                                     len(info0[0][0]) - 3:len(
                                                                                         info0[0][0])]
                            idraw.text((PosX, PosY + 18), info0output, font=font, fill='#ffffff')  # 1 0 0 0
                        else:
                            message_arr_output = message_arr[count][:len(message_arr[count]) - 3] + ' ' + message_arr[
                                                                                                              count][
                                                                                                          len(
                                                                                                              message_arr[
                                                                                                                  count]) - 3:len(
                                                                                                              message_arr[
                                                                                                                  count])]
                            idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6",
                                                    radius=7)
                            idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0 0 0

                PosX = PosX + 127
                if str(message_arr[count + 1]) == '-':
                    idraw.text((PosX + 22, PosY - 10), '_', font=font, fill="#a8a8a6")  # 1 0 0 0
                    idraw.text((PosX + 27, PosY - 10), '_', font=font, fill="#a8a8a6")  # Для жирности
                elif str(info1[0][0]) == '-':
                    if message_arr[count + 1].find('/') == -1:
                        message_arr_output = message_arr[count + 1][:len(message_arr[count + 1]) - 3] + ' ' + \
                                             message_arr[count + 1][
                                             len(message_arr[
                                                     count + 1]) - 3:len(
                                                 message_arr[
                                                     count + 1])]
                        idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6",
                                                radius=7)
                        idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0 0 0
                    else:
                        number_one = message_arr[count + 1][:message_arr[count + 1].find('/')]
                        number_two = message_arr[count + 1][message_arr[count + 1].find('/') + 1:]
                        message_arr_output0 = number_one[:len(number_one) - 3] + ' ' + number_one[
                                                                                       len(number_one) - 3:len(
                                                                                           number_one)]
                        message_arr_output1 = number_two[:len(number_two) - 3] + ' ' + number_two[
                                                                                       len(number_two) - 3:len(
                                                                                           number_two)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.rounded_rectangle((PosX - 7 - 35, PosY - 7, PosX - 7 + 80 + 35, PosY - 7 + 31),
                                                fill="#a8a8a6", radius=7)
                        idraw.text((PosX - 35, PosY), message_arr_output, font=font, fill='black')
                elif message_arr[count + 1].find('/') > 0:
                    number_one0 = info1[0][0][:info1[0][0].find('/')]
                    number_two0 = info1[0][0][info1[0][0].find('/') + 1:]
                    number_one = message_arr[count + 1][:message_arr[count + 1].find('/')]
                    number_two = message_arr[count + 1][message_arr[count + 1].find('/') + 1:]
                    if int(number_one0) == int(number_one):
                        message_arr_output0 = number_one[:len(number_one) - 3] + ' ' + number_one[
                                                                                       len(number_one) - 3:len(
                                                                                           number_one)]
                        message_arr_output1 = number_two[:len(number_two) - 3] + ' ' + number_two[
                                                                                       len(number_two) - 3:len(
                                                                                           number_two)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.rounded_rectangle((PosX - 7 - 35, PosY - 7, PosX - 7 + 80 + 35, PosY - 7 + 31),
                                                fill="#a8a8a6", radius=7)
                        idraw.text((PosX - 35, PosY), message_arr_output, font=font, fill='black')
                    elif int(number_one0) < int(number_one):
                        message_arr_output0 = number_one[:len(number_one) - 3] + ' ' + number_one[
                                                                                       len(number_one) - 3:len(
                                                                                           number_one)]
                        message_arr_output1 = number_two[:len(number_two) - 3] + ' ' + number_two[
                                                                                       len(number_two) - 3:len(
                                                                                           number_two)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.rounded_rectangle((PosX - 7 - 35, PosY - 7 - 10, PosX - 7 + 80 + 35, PosY - 7 + 31 - 10),
                                                fill="#67a947", radius=7)
                        idraw.text((PosX - 35, PosY - 10), message_arr_output, font=font, fill='#ffffff')
                        message_arr_output0 = number_one0[:len(number_one0) - 3] + ' ' + number_one0[
                                                                                         len(number_one0) - 3:len(
                                                                                             number_one0)]
                        message_arr_output1 = number_two0[:len(number_two0) - 3] + ' ' + number_two0[
                                                                                         len(number_two0) - 3:len(
                                                                                             number_two0)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.text((PosX - 35, PosY + 17), message_arr_output, font=font, fill='#ffffff')

                    elif int(number_one0) > int(number_one):
                        message_arr_output0 = number_one[:len(number_one) - 3] + ' ' + number_one[
                                                                                       len(number_one) - 3:len(
                                                                                           number_one)]
                        message_arr_output1 = number_two[:len(number_two) - 3] + ' ' + number_two[
                                                                                       len(number_two) - 3:len(
                                                                                           number_two)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.rounded_rectangle((PosX - 7 - 35, PosY - 7 - 10, PosX - 7 + 80 + 35, PosY - 7 + 31 - 10),
                                                fill="#ac4540", radius=7)
                        idraw.text((PosX - 35, PosY - 10), message_arr_output, font=font, fill='#ffffff')
                        message_arr_output0 = number_one0[:len(number_one0) - 3] + ' ' + number_one0[
                                                                                         len(number_one0) - 3:len(
                                                                                             number_one0)]
                        message_arr_output1 = number_two0[:len(number_two0) - 3] + ' ' + number_two0[
                                                                                         len(number_two0) - 3:len(
                                                                                             number_two0)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.text((PosX - 35, PosY + 17), message_arr_output, font=font, fill='#ffffff')
                else:
                    if int(info1[0][0]) == int(message_arr[count + 1]):
                        message_arr_output = message_arr[count + 1][:len(message_arr[count + 1]) - 3] + ' ' + \
                                             message_arr[count + 1][
                                             len(message_arr[
                                                     count + 1]) - 3:len(
                                                 message_arr[
                                                     count + 1])]
                        idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6",
                                                radius=7)
                        idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0 0 0
                    elif int(info1[0][0]) < int(message_arr[count + 1]):
                        if str(info1[0][0]) != '-':
                            message_arr_output = message_arr[count + 1][:len(message_arr[count + 1]) - 3] + ' ' + \
                                                 message_arr[
                                                     count + 1][len(
                                                     message_arr[count + 1]) - 3:len(message_arr[count + 1])]
                            idraw.rounded_rectangle((PosX - 7, PosY - 12 - 7, PosX - 7 + 80, PosY - 12 - 7 + 31),
                                                    fill="#67a947", radius=7)
                            idraw.text((PosX, PosY - 12), message_arr_output, font=font, fill='#ffffff')  # 1 0 0 0
                            idraw.text((PosX + 1, PosY - 12), message_arr_output, font=font,
                                       fill='#ffffff')  # Для жирности
                            info0output = info1[0][0][:len(info1[0][0]) - 3] + ' ' + info1[0][0][
                                                                                     len(info1[0][0]) - 3:len(
                                                                                         info1[0][0])]
                            idraw.text((PosX, PosY + 18), info0output, font=font, fill='#ffffff')  # 1 0 0 0
                        else:
                            message_arr_output = message_arr[count + 1][:len(message_arr[count + 1]) - 3] + ' ' + \
                                                 message_arr[
                                                     count + 1][len(
                                                     message_arr[count + 1]) - 3:len(message_arr[count + 1])]
                            idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6",
                                                    radius=7)
                            idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0 0 0
                    elif int(info1[0][0]) > int(message_arr[count + 1]):
                        if str(info1[0][0]) != '-':
                            message_arr_output = message_arr[count + 1][:len(message_arr[count + 1]) - 3] + ' ' + \
                                                 message_arr[
                                                     count + 1][len(
                                                     message_arr[count + 1]) - 3:len(message_arr[count + 1])]
                            idraw.rounded_rectangle((PosX - 7, PosY - 12 - 7, PosX - 7 + 80, PosY - 12 - 7 + 31),
                                                    fill="#ac4540", radius=7)
                            idraw.text((PosX, PosY - 12), message_arr_output, font=font, fill='#ffffff')  # 1 0 0 0
                            idraw.text((PosX + 1, PosY - 12), message_arr_output, font=font,
                                       fill='#ffffff')  # Для жирности
                            info0output = info1[0][0][:len(info1[0][0]) - 3] + ' ' + info1[0][0][
                                                                                     len(info1[0][0]) - 3:len(
                                                                                         info1[0][0])]
                            idraw.text((PosX, PosY + 18), info0output, font=font, fill='#ffffff')  # 1 0 0 0
                        else:
                            message_arr_output = message_arr[count + 1][:len(message_arr[count + 1]) - 3] + ' ' + \
                                                 message_arr[
                                                     count + 1][len(
                                                     message_arr[count + 1]) - 3:len(message_arr[count + 1])]
                            idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6",
                                                    radius=7)
                            idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0 0 0

                PosX = PosX + 127
                if str(message_arr[count + 2]) == '-':
                    idraw.text((PosX + 22, PosY - 10), '_', font=font, fill="#a8a8a6")  # 1 0 0 0
                    idraw.text((PosX + 27, PosY - 10), '_', font=font, fill="#a8a8a6")  # Для жирности
                elif str(info2[0][0]) == '-':
                    if message_arr[count + 2].find('/') == -1:
                        message_arr_output = message_arr[count + 2][:len(message_arr[count + 2]) - 3] + ' ' + \
                                             message_arr[count + 2][
                                             len(message_arr[
                                                     count + 2]) - 3:len(
                                                 message_arr[
                                                     count + 2])]
                        idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6",
                                                radius=7)
                        idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0 0 0
                    else:
                        number_one = message_arr[count + 2][:message_arr[count + 2].find('/')]
                        number_two = message_arr[count + 2][message_arr[count + 2].find('/') + 1:]
                        message_arr_output0 = number_one[:len(number_one) - 3] + ' ' + number_one[
                                                                                       len(number_one) - 3:len(
                                                                                           number_one)]
                        message_arr_output1 = number_two[:len(number_two) - 3] + ' ' + number_two[
                                                                                       len(number_two) - 3:len(
                                                                                           number_two)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.rounded_rectangle((PosX - 7 - 35, PosY - 7, PosX - 7 + 80 + 35, PosY - 7 + 31),
                                                fill="#a8a8a6", radius=7)
                        idraw.text((PosX - 35, PosY), message_arr_output, font=font, fill='black')
                elif message_arr[count + 2].find('/') > 0:
                    number_one0 = info2[0][0][:info2[0][0].find('/')]
                    number_two0 = info2[0][0][info2[0][0].find('/') + 1:]
                    number_one = message_arr[count + 2][:message_arr[count + 2].find('/')]
                    number_two = message_arr[count + 2][message_arr[count + 2].find('/') + 1:]
                    if int(number_one0) == int(number_one):
                        message_arr_output0 = number_one[:len(number_one) - 3] + ' ' + number_one[
                                                                                       len(number_one) - 3:len(
                                                                                           number_one)]
                        message_arr_output1 = number_two[:len(number_two) - 3] + ' ' + number_two[
                                                                                       len(number_two) - 3:len(
                                                                                           number_two)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.rounded_rectangle((PosX - 7 - 35, PosY - 7, PosX - 7 + 80 + 35, PosY - 7 + 31),
                                                fill="#a8a8a6", radius=7)
                        idraw.text((PosX - 35, PosY), message_arr_output, font=font, fill='black')
                    elif int(number_one0) < int(number_one):
                        message_arr_output0 = number_one[:len(number_one) - 3] + ' ' + number_one[
                                                                                       len(number_one) - 3:len(
                                                                                           number_one)]
                        message_arr_output1 = number_two[:len(number_two) - 3] + ' ' + number_two[
                                                                                       len(number_two) - 3:len(
                                                                                           number_two)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.rounded_rectangle((PosX - 7 - 35, PosY - 7 - 10, PosX - 7 + 80 + 35, PosY - 7 + 31 - 10),
                                                fill="#67a947", radius=7)
                        idraw.text((PosX - 35, PosY - 10), message_arr_output, font=font, fill='#ffffff')
                        message_arr_output0 = number_one0[:len(number_one0) - 3] + ' ' + number_one0[
                                                                                         len(number_one0) - 3:len(
                                                                                             number_one0)]
                        message_arr_output1 = number_two0[:len(number_two0) - 3] + ' ' + number_two0[
                                                                                         len(number_two0) - 3:len(
                                                                                             number_two0)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.text((PosX - 35, PosY + 17), message_arr_output, font=font, fill='#ffffff')

                    elif int(number_one0) > int(number_one):
                        message_arr_output0 = number_one[:len(number_one) - 3] + ' ' + number_one[
                                                                                       len(number_one) - 3:len(
                                                                                           number_one)]
                        message_arr_output1 = number_two[:len(number_two) - 3] + ' ' + number_two[
                                                                                       len(number_two) - 3:len(
                                                                                           number_two)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.rounded_rectangle((PosX - 7 - 35, PosY - 7 - 10, PosX - 7 + 80 + 35, PosY - 7 + 31 - 10),
                                                fill="#ac4540", radius=7)
                        idraw.text((PosX - 35, PosY - 10), message_arr_output, font=font, fill='#ffffff')
                        message_arr_output0 = number_one0[:len(number_one0) - 3] + ' ' + number_one0[
                                                                                         len(number_one0) - 3:len(
                                                                                             number_one0)]
                        message_arr_output1 = number_two0[:len(number_two0) - 3] + ' ' + number_two0[
                                                                                         len(number_two0) - 3:len(
                                                                                             number_two0)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.text((PosX - 35, PosY + 17), message_arr_output, font=font, fill='#ffffff')
                else:
                    if int(info2[0][0]) == int(message_arr[count + 2]):
                        message_arr_output = message_arr[count + 2][:len(message_arr[count + 2]) - 3] + ' ' + \
                                             message_arr[count + 2][
                                             len(message_arr[
                                                     count + 2]) - 3:len(
                                                 message_arr[
                                                     count + 2])]
                        idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6",
                                                radius=7)
                        idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0 0 0
                    elif int(info2[0][0]) < int(message_arr[count + 2]):
                        if str(info2[0][0]) != '-':
                            message_arr_output = message_arr[count + 2][:len(message_arr[count + 2]) - 3] + ' ' + \
                                                 message_arr[
                                                     count + 2][len(
                                                     message_arr[count + 2]) - 3:len(message_arr[count + 2])]
                            idraw.rounded_rectangle((PosX - 7, PosY - 12 - 7, PosX - 7 + 80, PosY - 12 - 7 + 31),
                                                    fill="#67a947", radius=7)
                            idraw.text((PosX, PosY - 12), message_arr_output, font=font, fill='#ffffff')  # 1 0 0 0
                            idraw.text((PosX + 1, PosY - 12), message_arr_output, font=font,
                                       fill='#ffffff')  # Для жирности
                            info0output = info2[0][0][:len(info2[0][0]) - 3] + ' ' + info2[0][0][
                                                                                     len(info2[0][0]) - 3:len(
                                                                                         info2[0][0])]
                            idraw.text((PosX, PosY + 18), info0output, font=font, fill='#ffffff')  # 1 0 0 0
                        else:
                            message_arr_output = message_arr[count + 2][:len(message_arr[count + 2]) - 3] + ' ' + \
                                                 message_arr[
                                                     count + 2][len(
                                                     message_arr[count + 2]) - 3:len(message_arr[count + 2])]
                            idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6",
                                                    radius=7)
                            idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0 0 0
                    elif int(info2[0][0]) > int(message_arr[count + 2]):
                        if str(info2[0][0]) != '-':
                            message_arr_output = message_arr[count + 2][:len(message_arr[count + 2]) - 3] + ' ' + \
                                                 message_arr[
                                                     count + 2][len(
                                                     message_arr[count + 2]) - 3:len(message_arr[count + 2])]
                            idraw.rounded_rectangle((PosX - 7, PosY - 12 - 7, PosX - 7 + 80, PosY - 12 - 7 + 31),
                                                    fill="#ac4540", radius=7)
                            idraw.text((PosX, PosY - 12), message_arr_output, font=font, fill='#ffffff')  # 1 0 0 0
                            idraw.text((PosX + 1, PosY - 12), message_arr_output, font=font,
                                       fill='#ffffff')  # Для жирности
                            info0output = info2[0][0][:len(info2[0][0]) - 3] + ' ' + info2[0][0][
                                                                                     len(info2[0][0]) - 3:len(
                                                                                         info2[0][0])]
                            idraw.text((PosX, PosY + 18), info0output, font=font, fill='#ffffff')  # 1 0 0 0
                        else:
                            message_arr_output = message_arr[count + 2][:len(message_arr[count + 2]) - 3] + ' ' + \
                                                 message_arr[
                                                     count + 2][len(
                                                     message_arr[count + 2]) - 3:len(message_arr[count + 2])]
                            idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6",
                                                    radius=7)
                            idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0 0 0

                PosX = PosX + 127
                if str(message_arr[count + 3]) == '-':
                    idraw.text((PosX + 22, PosY - 10), '_', font=font, fill="#a8a8a6")  # 1 0 0 0
                    idraw.text((PosX + 27, PosY - 10), '_', font=font, fill="#a8a8a6")  # Для жирности
                elif str(info3[0][0]) == '-':
                    if message_arr[count + 3].find('/') == -1:
                        message_arr_output = message_arr[count + 3][:len(message_arr[count + 3]) - 3] + ' ' + \
                                             message_arr[count + 3][
                                             len(message_arr[
                                                     count + 3]) - 3:len(
                                                 message_arr[
                                                     count + 3])]
                        idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6",
                                                radius=7)
                        idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0 0 0
                    else:
                        number_one = message_arr[count + 3][:message_arr[count + 3].find('/')]
                        number_two = message_arr[count + 3][message_arr[count + 3].find('/') + 1:]
                        message_arr_output0 = number_one[:len(number_one) - 3] + ' ' + number_one[
                                                                                       len(number_one) - 3:len(
                                                                                           number_one)]
                        message_arr_output1 = number_two[:len(number_two) - 3] + ' ' + number_two[
                                                                                       len(number_two) - 3:len(
                                                                                           number_two)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.rounded_rectangle((PosX - 7 - 35, PosY - 7, PosX - 7 + 80 + 35, PosY - 7 + 31),
                                                fill="#a8a8a6", radius=7)
                        idraw.text((PosX - 35, PosY), message_arr_output, font=font, fill='black')
                elif message_arr[count + 3].find('/') > 0:
                    number_one0 = info3[0][0][:info3[0][0].find('/')]
                    number_two0 = info3[0][0][info3[0][0].find('/') + 1:]
                    number_one = message_arr[count + 3][:message_arr[count + 3].find('/')]
                    number_two = message_arr[count + 3][message_arr[count + 3].find('/') + 1:]
                    if int(number_one0) == int(number_one):
                        message_arr_output0 = number_one[:len(number_one) - 3] + ' ' + number_one[
                                                                                       len(number_one) - 3:len(
                                                                                           number_one)]
                        message_arr_output1 = number_two[:len(number_two) - 3] + ' ' + number_two[
                                                                                       len(number_two) - 3:len(
                                                                                           number_two)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.rounded_rectangle((PosX - 7 - 35, PosY - 7, PosX - 7 + 80 + 35, PosY - 7 + 31),
                                                fill="#a8a8a6", radius=7)
                        idraw.text((PosX - 35, PosY), message_arr_output, font=font, fill='black')
                    elif int(number_one0) < int(number_one):
                        message_arr_output0 = number_one[:len(number_one) - 3] + ' ' + number_one[
                                                                                       len(number_one) - 3:len(
                                                                                           number_one)]
                        message_arr_output1 = number_two[:len(number_two) - 3] + ' ' + number_two[
                                                                                       len(number_two) - 3:len(
                                                                                           number_two)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.rounded_rectangle((PosX - 7 - 35, PosY - 7 - 10, PosX - 7 + 80 + 35, PosY - 7 + 31 - 10),
                                                fill="#67a947", radius=7)
                        idraw.text((PosX - 35, PosY - 10), message_arr_output, font=font, fill='#ffffff')
                        message_arr_output0 = number_one0[:len(number_one0) - 3] + ' ' + number_one0[
                                                                                         len(number_one0) - 3:len(
                                                                                             number_one0)]
                        message_arr_output1 = number_two0[:len(number_two0) - 3] + ' ' + number_two0[
                                                                                         len(number_two0) - 3:len(
                                                                                             number_two0)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.text((PosX - 35, PosY + 17), message_arr_output, font=font, fill='#ffffff')

                    elif int(number_one0) > int(number_one):
                        message_arr_output0 = number_one[:len(number_one) - 3] + ' ' + number_one[
                                                                                       len(number_one) - 3:len(
                                                                                           number_one)]
                        message_arr_output1 = number_two[:len(number_two) - 3] + ' ' + number_two[
                                                                                       len(number_two) - 3:len(
                                                                                           number_two)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.rounded_rectangle((PosX - 7 - 35, PosY - 7 - 10, PosX - 7 + 80 + 35, PosY - 7 + 31 - 10),
                                                fill="#ac4540", radius=7)
                        idraw.text((PosX - 35, PosY - 10), message_arr_output, font=font, fill='#ffffff')
                        message_arr_output0 = number_one0[:len(number_one0) - 3] + ' ' + number_one0[
                                                                                         len(number_one0) - 3:len(
                                                                                             number_one0)]
                        message_arr_output1 = number_two0[:len(number_two0) - 3] + ' ' + number_two0[
                                                                                         len(number_two0) - 3:len(
                                                                                             number_two0)]
                        message_arr_output = message_arr_output0 + '/' + message_arr_output1
                        idraw.text((PosX - 35, PosY + 17), message_arr_output, font=font, fill='#ffffff')
                else:
                    if int(info3[0][0]) == int(message_arr[count + 3]):
                        message_arr_output = message_arr[count + 3][:len(message_arr[count]) - 3] + ' ' + message_arr[
                                                                                                              count + 3][
                                                                                                          len(
                                                                                                              message_arr[
                                                                                                                  count + 3]) - 3:len(
                                                                                                              message_arr[
                                                                                                                  count + 3])]
                        idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6",
                                                radius=7)
                        idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0 0 0
                    elif int(info3[0][0]) < int(message_arr[count + 3]):
                        if str(info3[0][0]) != '-':
                            message_arr_output = message_arr[count + 3][:len(message_arr[count + 3]) - 3] + ' ' + \
                                                 message_arr[
                                                     count + 3][len(
                                                     message_arr[count + 3]) - 3:len(message_arr[count + 3])]
                            idraw.rounded_rectangle((PosX - 7, PosY - 12 - 7, PosX - 7 + 80, PosY - 12 - 7 + 31),
                                                    fill="#67a947", radius=7)
                            idraw.text((PosX, PosY - 12), message_arr_output, font=font, fill='#ffffff')  # 1 0 0 0
                            idraw.text((PosX + 1, PosY - 12), message_arr_output, font=font,
                                       fill='#ffffff')  # Для жирности
                            info0output = info3[0][0][:len(info3[0][0]) - 3] + ' ' + info3[0][0][
                                                                                     len(info3[0][0]) - 3:len(
                                                                                         info3[0][0])]
                            idraw.text((PosX, PosY + 18), info0output, font=font, fill='#ffffff')  # 1 0 0 0
                        else:
                            message_arr_output = message_arr[count + 3][:len(message_arr[count + 3]) - 3] + ' ' + \
                                                 message_arr[
                                                     count + 3][len(
                                                     message_arr[count + 3]) - 3:len(message_arr[count + 3])]
                            idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6",
                                                    radius=7)
                            idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0 0 0
                    elif int(info3[0][0]) > int(message_arr[count + 3]):
                        if str(info3[0][0]) != '-':
                            message_arr_output = message_arr[count + 3][:len(message_arr[count + 3]) - 3] + ' ' + \
                                                 message_arr[
                                                     count + 3][len(
                                                     message_arr[count + 3]) - 3:len(message_arr[count + 3])]
                            idraw.rounded_rectangle((PosX - 7, PosY - 12 - 7, PosX - 7 + 80, PosY - 12 - 7 + 31),
                                                    fill="#ac4540", radius=7)
                            idraw.text((PosX, PosY - 12), message_arr_output, font=font, fill='#ffffff')  # 1 0 0 0
                            idraw.text((PosX + 1, PosY - 12), message_arr_output, font=font,
                                       fill='#ffffff')  # Для жирности
                            info0output = info3[0][0][:len(info3[0][0]) - 3] + ' ' + info3[0][0][
                                                                                     len(info3[0][0]) - 3:len(
                                                                                         info3[0][0])]
                            idraw.text((PosX, PosY + 18), info0output, font=font, fill='#ffffff')  # 1 0 0 0
                        else:
                            message_arr_output = message_arr[count + 3][:len(message_arr[count + 3]) - 3] + ' ' + \
                                                 message_arr[
                                                     count + 3][len(
                                                     message_arr[count + 3]) - 3:len(message_arr[count + 3])]
                            idraw.rounded_rectangle((PosX - 7, PosY - 7, PosX - 7 + 80, PosY - 7 + 31), fill="#a8a8a6",
                                                    radius=7)
                            idraw.text((PosX, PosY), message_arr_output, font=font, fill='black')  # 1 0 0 0

                if count_db_table == 2 or count_db_table == 3:
                    PosY += 78
                if count_db_table == 1:
                    PosY += 81
                PosX = 497

                cur.execute('DROP TABLE line' + str(count_db_table))
                base.commit()
                base.execute('CREATE TABLE IF NOT EXISTS line' + str(count_db_table) + '(info0, info1, info2, info3)')
                base.commit()
                cur.execute('INSERT INTO line' + str(count_db_table) + ' VALUES(?, ?, ?, ?)', (
                message_arr[count], message_arr[count + 1], message_arr[count + 2], message_arr[count + 3]))
                base.commit()
                base.execute('CREATE TABLE IF NOT EXISTS DBlinePlot' + str(
                    count_db_table) + '(date, info0, info1, info2, info3)')
                base.commit()
                cur.execute('INSERT INTO DBlinePlot' + str(count_db_table) + ' VALUES(?, ?, ?, ?, ?)', (
                message_arr[1], message_arr[count], message_arr[count + 1], message_arr[count + 2],
                message_arr[count + 3]))
                base.commit()
                count_db_table += 1
                count += 4
            image.save('png/ЭкспортИтог.png')
            image0 = open('png/ЭкспортИтог.png', 'rb')
        await bot.send_photo(id, image0)

    # Дашборд
    if str(message_arr[0]) == 'Дашборд':
        base = sqlite3.connect('db/PhotoDashbord.db')
        cur = base.cursor()
        image = Image.open("png/ДашбордФон.png")
        image = image.resize((720, 1280))
        count = 2
        while count < len(message_arr):
            message_arr[count] = message_arr[count].replace(',', '.')
            count += 1

        # Блок со спидометром
        image_strelka = Image.open("png/Стрелка.png")
        idraw = ImageDraw.Draw(image)
        MAX_SIZE = (220, 220)
        image_strelka.thumbnail(MAX_SIZE)
        image_strelka = image_strelka.rotate(90)
        angle = round(int(message_arr[4]) * (-9) / 5)
        image_strelka = image_strelka.rotate(angle)
        image.paste(image_strelka, (426, 428), mask=image_strelka)
        idraw.arc(xy=(425, 435, 646, 657), start=180, end=360, fill='white', width=2)

        # Дата
        font = ImageFont.truetype("ttf/articulat-cf-extra-light.ttf", size=30)
        idraw.text((518, 192), message_arr[1], font=font)

        # Блок с курсом валют
        info_dollar = cur.execute('SELECT info0 FROM Valuta').fetchall()
        info_evro = cur.execute('SELECT info1 FROM Valuta').fetchall()
        # Доллар
        font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=28)
        text = message_arr[2].replace('.', ',')
        idraw.text((166, 426), text, font=font, fill='#ffffff')
        if float(info_dollar[0][0]) == float(message_arr[2]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=26)
            idraw.rounded_rectangle((255, 419, 351, 456), fill="#c8c4bb", radius=7)
            idraw.text((272, 426), '0,0%', font=font, fill='#ffffff')
        elif float(info_dollar[0][0]) < float(message_arr[2]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=26)
            idraw.rounded_rectangle((255, 419, 351, 456), fill="#77a658", radius=7)
            percent = str(round(((float(message_arr[2]) / float(info_dollar[0][0])) * 100 - 100), 2))
            percent = percent.replace('.', ',')
            idraw.text((262, 426), '+' + percent + '%', font=font, fill='#ffffff')
        elif float(info_dollar[0][0]) > float(message_arr[2]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=26)
            idraw.rounded_rectangle((255, 419, 351, 456), fill="#ce5950", radius=7)
            percent = str(round(((float(message_arr[2]) / float(info_dollar[0][0])) * 100 - 100), 2))
            percent = percent.replace('.', ',')
            idraw.text((262, 426), percent + '%', font=font, fill='#ffffff')
        # Евро
        font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=28)
        text = message_arr[3].replace('.', ',')
        idraw.text((166, 516), text, font=font, fill='#ffffff')
        if float(info_evro[0][0]) == float(message_arr[3]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=26)
            idraw.rounded_rectangle((255, 509, 351, 546), fill="#c8c4bb", radius=7)
            idraw.text((272, 516), '0,0%', font=font, fill='#ffffff')
        elif float(info_evro[0][0]) < float(message_arr[3]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=26)
            idraw.rounded_rectangle((255, 509, 351, 546), fill="#77a658", radius=7)
            percent = str(round(((float(message_arr[3]) / float(info_evro[0][0])) * 100 - 100), 2))
            percent = percent.replace('.', ',')
            idraw.text((262, 516), '+' + percent + '%', font=font, fill='#ffffff')
        elif float(info_evro[0][0]) > float(message_arr[3]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=26)
            idraw.rounded_rectangle((255, 509, 351, 546), fill="ce5950", radius=7)
            percent = str(round(((float(message_arr[3]) / float(info_evro[0][0])) * 100 - 100), 2))
            percent = percent.replace('.', ',')
            idraw.text((262, 516), percent + '%', font=font, fill='#ffffff')
        cur.execute('DROP TABLE Valuta')
        base.commit()
        base.execute('CREATE TABLE IF NOT EXISTS Valuta(info0, info1)')
        base.commit()
        cur.execute('INSERT INTO Valuta VALUES(?, ?)', (message_arr[2], message_arr[3]))
        base.commit()

        # Фьючерсы свот
        info_psheno = cur.execute('SELECT info0 FROM Futchersi').fetchall()
        info_kukuruza = cur.execute('SELECT info1 FROM Futchersi').fetchall()
        info_soy = cur.execute('SELECT info2 FROM Futchersi').fetchall()
        # Пшеница
        font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=22)
        text = message_arr[5].replace('.', ',')
        idraw.text((64, 815), text + '$', font=font, fill='#ffffff')
        if float(info_psheno[0][0]) == float(message_arr[5]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((57, 850, 152, 879), fill="#c8c4bb", radius=7)
            idraw.text((75, 857), '0,0$/т', font=font, fill='#ffffff')
        elif float(info_psheno[0][0]) < float(message_arr[5]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((57, 850, 152, 879), fill="#77a658", radius=7)
            percent = str(round(float(message_arr[5]) - float(info_psheno[0][0]), 2))
            percent = percent.replace('.', ',')
            idraw.text((60, 857), '+' + percent + '$/т', font=font, fill='#ffffff')
        elif float(info_psheno[0][0]) > float(message_arr[5]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((57, 850, 152, 879), fill="#ce5950", radius=7)
            percent = str(round(float(message_arr[5]) - float(info_psheno[0][0]), 2))
            percent = percent.replace('.', ',')
            idraw.text((60, 857), percent + '$/т', font=font, fill='#ffffff')
        # Кукуруза
        font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=22)
        text = message_arr[6].replace('.', ',')
        idraw.text((167, 815), text + '$', font=font, fill='#ffffff')
        if float(info_kukuruza[0][0]) == float(message_arr[6]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((160, 850, 255, 879), fill="#c8c4bb", radius=7)
            idraw.text((178, 857), '0,0$/т', font=font, fill='#ffffff')
        elif float(info_kukuruza[0][0]) < float(message_arr[6]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((160, 850, 255, 879), fill="#77a658", radius=7)
            percent = str(round(float(message_arr[6]) - float(info_kukuruza[0][0]), 2))
            percent = percent.replace('.', ',')
            idraw.text((163, 857), '+' + percent + '$/т', font=font, fill='#ffffff')
        elif float(info_kukuruza[0][0]) > float(message_arr[6]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((160, 850, 255, 879), fill="#ce5950", radius=7)
            percent = str(round(float(message_arr[6]) - float(info_kukuruza[0][0]), 2))
            percent = percent.replace('.', ',')
            idraw.text((163, 857), percent + '$/т', font=font, fill='#ffffff')
        # Соя
        font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=22)
        text = message_arr[7].replace('.', ',')
        idraw.text((269, 815), text + '$', font=font, fill='#ffffff')
        if float(info_soy[0][0]) == float(message_arr[7]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((262, 850, 357, 879), fill="#c8c4bb", radius=7)
            idraw.text((280, 857), '0,0$/т', font=font, fill='#ffffff')
        elif float(info_soy[0][0]) < float(message_arr[7]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((262, 850, 357, 879), fill="#77a658", radius=7)
            percent = str(round(float(message_arr[7]) - float(info_soy[0][0]), 2))
            percent = percent.replace('.', ',')
            idraw.text((265, 857), '+' + percent + '$/т', font=font, fill='#ffffff')
        elif float(info_soy[0][0]) > float(message_arr[7]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((262, 850, 357, 879), fill="#ce5950", radius=7)
            percent = str(round(float(message_arr[7]) - float(info_soy[0][0]), 2))
            percent = percent.replace('.', ',')
            idraw.text((265, 857), percent + '$/т', font=font, fill='#ffffff')
        cur.execute('DROP TABLE Futchersi')
        base.commit()
        base.execute('CREATE TABLE IF NOT EXISTS Futchersi(info0, info1, info2)')
        base.commit()
        cur.execute('INSERT INTO Futchersi VALUES(?, ?, ?)', (message_arr[5], message_arr[6], message_arr[7]))
        base.commit()

        # Прогноз экспортных пошлин
        if message_arr[8][2] == '.':
            cur.execute('DROP TABLE PoshlinaData')
            base.commit()
            base.execute('CREATE TABLE IF NOT EXISTS PoshlinaData(info0, info1)')
            base.commit()
            cur.execute('INSERT INTO PoshlinaData VALUES(?, ?)', ('0', message_arr[8]))
            base.commit()
            count = 8
            while count < len(message_arr) - 1:
                message_arr[count] = message_arr[count + 1]
                count += 1
        info_poshlinadata = cur.execute('SELECT info1 FROM PoshlinaData').fetchall()
        font = ImageFont.truetype("ttf/ArgentCFSuper.ttf", size=21)
        idraw.text((567, 636), info_poshlinadata[0][0], font=font, fill='#ffffff')

        info_psheno = cur.execute('SELECT info0 FROM Poshlina').fetchall()
        info_ichmen = cur.execute('SELECT info1 FROM Poshlina').fetchall()
        info_kukuruza = cur.execute('SELECT info2 FROM Poshlina').fetchall()
        # Пшеница
        font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=20)
        text = message_arr[8].replace('.', ',')
        text = text[:1] + ' ' + text[1:]
        idraw.text((390, 816), text + 'Р', font=font, fill='#ffffff')
        if float(info_psheno[0][0]) == float(message_arr[8]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((389, 850, 483, 880), fill="#c8c4bb", radius=7)
            idraw.text((417, 858), '0,0Р', font=font, fill='#ffffff')
        elif float(info_psheno[0][0]) < float(message_arr[8]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((389, 850, 479, 880), fill="#77a658", radius=7)
            percent = str(round(float(message_arr[8]) - float(info_psheno[0][0]), 2))
            percent = percent.replace('.', ',')
            idraw.text((396, 858), '+' + percent + 'Р', font=font, fill='#ffffff')
        elif float(info_psheno[0][0]) > float(message_arr[8]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((389, 850, 479, 880), fill="#ce5950", radius=7)
            percent = str(round(float(message_arr[8]) - float(info_psheno[0][0]), 2))
            percent = percent.replace('.', ',')
            idraw.text((396, 858), percent + 'Р', font=font, fill='#ffffff')
        # Ячмень
        font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=20)
        text = message_arr[9].replace('.', ',')
        text = text[:1] + ' ' + text[1:]
        idraw.text((490, 815), text + 'Р', font=font, fill='#ffffff')
        if float(info_ichmen[0][0]) == float(message_arr[9]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((489, 850, 583, 880), fill="#c8c4bb", radius=7)
            idraw.text((517, 858), '0,0Р', font=font, fill='#ffffff')
        elif float(info_ichmen[0][0]) < float(message_arr[9]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((489, 850, 583, 880), fill="#77a658", radius=7)
            percent = str(round(float(message_arr[9]) - float(info_ichmen[0][0]), 2))
            percent = percent.replace('.', ',')
            idraw.text((496, 858), '+' + percent + 'Р', font=font, fill='#ffffff')
        elif float(info_ichmen[0][0]) > float(message_arr[9]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((489, 850, 583, 880), fill="#ce5950", radius=7)
            percent = str(round(float(message_arr[9]) - float(info_ichmen[0][0]), 2))
            percent = percent.replace('.', ',')
            idraw.text((496, 858), percent + 'Р', font=font, fill='#ffffff')
        # Кукуруза
        font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=20)
        text = message_arr[10].replace('.', ',')
        text = text[:1] + ' ' + text[1:]
        idraw.text((590, 815), text + 'Р', font=font, fill='#ffffff')
        if float(info_kukuruza[0][0]) == float(message_arr[10]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((590, 850, 676, 880), fill="#c8c4bb", radius=7)
            idraw.text((615, 858), '0,0Р', font=font, fill='#ffffff')
        elif float(info_kukuruza[0][0]) < float(message_arr[10]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((590, 850, 676, 880), fill="#77a658", radius=7)
            percent = str(round(float(message_arr[10]) - float(info_kukuruza[0][0]), 2))
            percent = percent.replace('.', ',')
            idraw.text((596, 858), '+' + percent + 'Р', font=font, fill='#ffffff')
        elif float(info_kukuruza[0][0]) > float(message_arr[10]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=19)
            idraw.rounded_rectangle((590, 850, 676, 880), fill="#ce5950", radius=7)
            percent = str(round(float(message_arr[10]) - float(info_kukuruza[0][0]), 2))
            percent = percent.replace('.', ',')
            idraw.text((596, 858), percent + 'Р', font=font, fill='#ffffff')
        cur.execute('DROP TABLE Poshlina')
        base.commit()
        base.execute('CREATE TABLE IF NOT EXISTS Poshlina(info0, info1, info2)')
        base.commit()
        cur.execute('INSERT INTO Poshlina VALUES(?, ?, ?)', (message_arr[8], message_arr[9], message_arr[10]))
        base.commit()

        # СРТ Новороссийск
        info_CPT = cur.execute('SELECT info0 FROM CPT').fetchall()
        font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=23)
        message_arr_output = str(message_arr[11][:len(message_arr[11]) - 3] + ' ' + message_arr[11][
                                                                                    len(message_arr[11]) - 3:len(
                                                                                        message_arr[11])])
        idraw.text((231, 1074), message_arr_output + ' руб', font=font, fill='#ffffff')
        idraw.text((232, 1074), message_arr_output + ' руб', font=font, fill='#ffffff')
        if int(info_CPT[0][0]) == int(message_arr[11]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=20)
            idraw.rounded_rectangle((224, 1121, 350, 1150), fill="#c8c4bb", radius=7)
            idraw.text((254, 1128), '0,0 руб', font=font, fill='#ffffff')  # Увеличить по x
        elif int(info_CPT[0][0]) < int(message_arr[11]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=20)
            idraw.rounded_rectangle((224, 1121, 350, 1150), fill="#77a658", radius=7)
            percent = str(int(message_arr[11]) - int(info_CPT[0][0]))
            if len(percent) > 3:
                percent = str(percent[:len(percent) - 3] + ' ' + percent[len(percent) - 3:len(percent)])
            idraw.text((231, 1128), '+' + percent + ' руб', font=font, fill='#ffffff')
        elif int(info_CPT[0][0]) > int(message_arr[11]):
            font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=20)
            idraw.rounded_rectangle((224, 1121, 350, 1150), fill="#ce5950", radius=7)
            percent = str(int(message_arr[11]) - int(info_CPT[0][0]))
            if len(percent) > 4:
                percent = str(percent[:len(percent) - 3] + ' ' + percent[len(percent) - 3:len(percent)])
            idraw.text((231, 1128), percent + ' руб', font=font, fill='#ffffff')
        cur.execute('DROP TABLE CPT')
        base.commit()
        base.execute('CREATE TABLE IF NOT EXISTS CPT(info0, info1)')
        base.commit()
        cur.execute('INSERT INTO CPT VALUES(?, ?)', (message_arr[11], 0))
        base.commit()

        # Индекс логистики график первый
        info_count = cur.execute('SELECT info0 FROM Plot1').fetchall()
        cur.execute('INSERT INTO Plot1 VALUES(?, ?)', (info_count[len(info_count) - 1][0] + 1, message_arr[12]))
        base.commit()
        font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=20)
        info_plot1 = cur.execute('SELECT info1 FROM Plot1').fetchall()
        if info_plot1[len(info_plot1) - 2][0] == info_plot1[len(info_plot1) - 1][0]:
            idraw.text((465, 1038), message_arr[12], font=font, fill='#ffffff')
        elif info_plot1[len(info_plot1) - 2][0] < info_plot1[len(info_plot1) - 1][0]:
            idraw.text((465, 1038), message_arr[12], font=font, fill='#77a658')
        elif info_plot1[len(info_plot1) - 2][0] > info_plot1[len(info_plot1) - 1][0]:
            idraw.text((465, 1038), message_arr[12], font=font, fill='#ce5950')
        count_info = len(info_plot1) - 1
        PosY = 1206 - round(int(info_plot1[count_info][0]) * 160 / 407)
        idraw.ellipse((672, PosY, 674, PosY + 2), '#fcc666')
        PosX = 669
        count = 0
        while count < 50:
            PosY_step = PosY
            point = int(info_plot1[count_info][0])
            point_next = int(info_plot1[count_info - 1][0])
            if point - point_next > 0:
                PosY = PosY + round(((point - point_next) * (7 / 20)))
                idraw.ellipse((PosX, PosY, PosX + 2, PosY + 2), '#fcc666')
            if point - point_next < 0:
                PosY = PosY - round((abs((point - point_next)) * (7 / 20)))
                idraw.ellipse((PosX, PosY, PosX + 2, PosY + 2), '#fcc666')
            if point - point_next == 0:
                PosY = PosY
            idraw.line((PosX + 1, PosY + 1, PosX + 4, PosY_step + 1), fill='#fcc666', width=3)
            PosX -= 3
            count_info -= 1
            count += 1

        # Индекс логистики график второй
        info_count = cur.execute('SELECT info0 FROM Plot2').fetchall()
        cur.execute('INSERT INTO Plot2 VALUES(?, ?)', (info_count[len(info_count) - 1][0] + 1, message_arr[13]))
        base.commit()
        font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=20)
        info_plot2 = cur.execute('SELECT info1 FROM Plot2').fetchall()
        if info_plot2[len(info_plot2) - 2][0] == info_plot2[len(info_plot2) - 1][0]:
            idraw.text((461, 1140), message_arr[13], font=font, fill='#ffffff')
        elif info_plot2[len(info_plot2) - 2][0] < info_plot2[len(info_plot2) - 1][0]:
            idraw.text((461, 1140), message_arr[13], font=font, fill='#77a658')
        elif info_plot2[len(info_plot2) - 2][0] > info_plot2[len(info_plot2) - 1][0]:
            idraw.text((461, 1140), message_arr[13], font=font, fill='#ce5950')
        count_info = len(info_plot2) - 1
        PosY = 1206 - round((int(info_plot2[count_info][0]) - 1844) / 18)
        idraw.ellipse((672, PosY, 674, PosY + 2), '#fcc666')
        PosX = 669
        count = 0
        while count < 50:
            PosY_step = PosY
            point = int(info_plot2[count_info][0])
            point_next = int(info_plot2[count_info - 1][0])
            if point - point_next > 0:
                PosY = PosY + round(((point - point_next) / 22))
                idraw.ellipse((PosX, PosY, PosX + 2, PosY + 2), '#fcc666')
            if point - point_next < 0:
                PosY = PosY - round((abs((point - point_next)) / 22))
                idraw.ellipse((PosX, PosY, PosX + 2, PosY + 2), '#fcc666')
            if point - point_next == 0:
                PosY = PosY
            idraw.line((PosX + 1, PosY + 1, PosX + 4, PosY_step + 1), fill='#fcc666', width=3)
            PosX -= 3
            count_info -= 1
            count += 1

        image = image.resize((1080, 1920))
        image.save('png/ДашбордИтог.png')
        image0 = open('png/ДашбордИтог.png', 'rb')
        await bot.send_photo(id, image0)

    # Карта
    if str(message_arr[0]) == 'Карта':
        base = sqlite3.connect('db/PhotoKarta.db')
        cur = base.cursor()
        image = Image.open("png/КартаФон.png")
        idraw = ImageDraw.Draw(image)

        font = ImageFont.truetype("ttf/articulat-cf-demi-bold.ttf", size=20)
        count_db_table = 1
        count = 1
        while count < 7:
            info1CFO = cur.execute('SELECT info0 FROM line' + str(count)).fetchall()
            info1PFO = cur.execute('SELECT info1 FROM line' + str(count)).fetchall()
            if count == 1:
                PosXCFO = 162
                PosYCFO = 125
                PosXPFO = 108
                PosYPFO = 265
            elif count == 2:
                PosXCFO = 622
                PosYCFO = 118
                PosXPFO = 566
                PosYPFO = 257
            elif count == 3:
                PosXCFO = 162
                PosYCFO = 558
                PosXPFO = 108
                PosYPFO = 707
            elif count == 4:
                PosXCFO = 622
                PosYCFO = 560
                PosXPFO = 566
                PosYPFO = 707
            elif count == 5:
                PosXCFO = 162
                PosYCFO = 983
                PosXPFO = 108
                PosYPFO = 1129
            elif count == 6:
                PosXCFO = 622
                PosYCFO = 983
                PosXPFO = 566
                PosYPFO = 1129
            # ЦФО
            if str(message_arr[count]) == '-':
                idraw.text((PosXCFO + 13, PosYCFO - 5), '_', font=font, fill="black")
                idraw.text((PosXCFO + 18, PosYCFO - 5), '_', font=font, fill="black")
            elif str(info1CFO[0][0]) == '-':
                message_arr_output = message_arr[count_db_table][:len(message_arr[count_db_table]) - 3] + ' ' + message_arr[count_db_table][len(message_arr[count_db_table]) - 3:len(message_arr[count_db_table])]
                idraw.text((PosXCFO, PosYCFO), message_arr_output, font=font, fill='black')
                idraw.text((PosXCFO + 1, PosYCFO), message_arr_output, font=font, fill='black')  # Для жирности
            else:
                if int(info1CFO[0][0]) == int(message_arr[count_db_table]):
                    message_arr_output = message_arr[count_db_table][:len(message_arr[count_db_table]) - 3] + ' ' + message_arr[count_db_table][len(message_arr[count_db_table]) - 3:len(message_arr[count_db_table])]
                    idraw.text((PosXCFO, PosYCFO), message_arr_output, font=font, fill='black')
                    idraw.text((PosXCFO + 1, PosYCFO), message_arr_output, font=font, fill='black')  # Для жирности
                elif int(info1CFO[0][0]) < int(message_arr[count_db_table]):
                    if str(info1CFO[0][0]) != '-':
                        message_arr_output = message_arr[count_db_table][:len(message_arr[count_db_table]) - 3] + ' ' + message_arr[count_db_table][len(message_arr[count_db_table]) - 3:len(message_arr[count_db_table])]
                        idraw.text((PosXCFO, PosYCFO), message_arr_output, font=font, fill='green')
                        idraw.text((PosXCFO + 1, PosYCFO), message_arr_output, font=font, fill='green')  # Для жирности
                        info0output = info1CFO[0][0][:len(info1CFO[0][0]) - 3] + ' ' + info1CFO[0][0][len(info1CFO[0][0]) - 3:len(info1CFO[0][0])]
                        idraw.text((PosXCFO, PosYCFO + 15), info0output, font=font, fill='black')
                    else:
                        message_arr_output = message_arr[count_db_table][:len(message_arr[count_db_table]) - 3] + ' ' + message_arr[count_db_table][len(message_arr[count_db_table]) - 3:len(message_arr[count_db_table])]
                        idraw.text((PosXCFO, PosYCFO), message_arr_output, font=font, fill='black')
                        idraw.text((PosXCFO + 1, PosYCFO), message_arr_output, font=font, fill='black')  # Для жирности
                elif int(info1CFO[0][0]) > int(message_arr[count_db_table]):
                    if str(info1CFO[0][0]) != '-':
                        message_arr_output = message_arr[count_db_table][:len(message_arr[count_db_table]) - 3] + ' ' + message_arr[count_db_table][len(message_arr[count_db_table]) - 3:len(message_arr[count_db_table])]
                        idraw.text((PosXCFO, PosYCFO), message_arr_output, font=font, fill='red')
                        idraw.text((PosXCFO + 1, PosYCFO), message_arr_output, font=font, fill='red')  # Для жирности
                        info0output = info1CFO[0][0][:len(info1CFO[0][0]) - 3] + ' ' + info1CFO[0][0][len(info1CFO[0][0]) - 3:len(info1CFO[0][0])]
                        idraw.text((PosXCFO, PosYCFO + 15), info0output, font=font, fill='black')
                    else:
                        message_arr_output = message_arr[count_db_table][:len(message_arr[count]) - 3] + ' ' + message_arr[count_db_table][len(message_arr[count_db_table]) - 3:len(message_arr[count_db_table])]
                        idraw.text((PosXCFO, PosYCFO), message_arr_output, font=font, fill='black')
                        idraw.text((PosXCFO + 1, PosYCFO), message_arr_output, font=font, fill='black')  # Для жирности
            # ПФО
            if str(message_arr[count_db_table + 1]) == '-':
                idraw.text((PosXPFO + 13, PosYPFO - 5), '_', font=font, fill="black")
                idraw.text((PosXPFO + 18, PosYPFO - 5), '_', font=font, fill="black")
            elif str(info1PFO[0][0]) == '-':
                message_arr_output = message_arr[count_db_table + 1][:len(message_arr[count_db_table + 1]) - 3] + ' ' + message_arr[count_db_table + 1][len(message_arr[count_db_table + 1]) - 3:len(message_arr[count_db_table + 1])]
                idraw.text((PosXPFO, PosYPFO), message_arr_output, font=font, fill='black')
                idraw.text((PosXPFO + 1, PosYPFO), message_arr_output, font=font, fill='black')  # Для жирности
            else:
                if int(info1PFO[0][0]) == int(message_arr[count_db_table + 1]):
                    message_arr_output = message_arr[count_db_table + 1][:len(message_arr[count_db_table + 1]) - 3] + ' ' + message_arr[count_db_table + 1][len(message_arr[count_db_table + 1]) - 3:len(message_arr[count_db_table + 1])]
                    idraw.text((PosXPFO, PosYPFO), message_arr_output, font=font, fill='black')
                    idraw.text((PosXPFO + 1, PosYPFO), message_arr_output, font=font, fill='black')  # Для жирности
                elif int(info1PFO[0][0]) < int(message_arr[count_db_table + 1]):
                    if str(info1PFO[0][0]) != '-':
                        message_arr_output = message_arr[count_db_table + 1][:len(message_arr[count_db_table + 1]) - 3] + ' ' + message_arr[count_db_table + 1][len(message_arr[count_db_table + 1]) - 3:len(message_arr[count_db_table + 1])]
                        idraw.text((PosXPFO, PosYPFO), message_arr_output, font=font, fill='green')
                        idraw.text((PosXPFO + 1, PosYPFO), message_arr_output, font=font, fill='green')  # Для жирности
                        info0output = info1PFO[0][0][:len(info1PFO[0][0]) - 3] + ' ' + info1PFO[0][0][len(info1PFO[0][0]) - 3:len(info1PFO[0][0])]
                        idraw.text((PosXPFO, PosYPFO + 15), info0output, font=font, fill='black')
                    else:
                        message_arr_output = message_arr[count_db_table + 1][:len(message_arr[count_db_table + 1]) - 3] + ' ' + message_arr[count_db_table + 1][len(message_arr[count_db_table + 1]) - 3:len(message_arr[count_db_table + 1])]
                        idraw.text((PosXPFO, PosYPFO), message_arr_output, font=font, fill='black')
                        idraw.text((PosXPFO + 1, PosYPFO), message_arr_output, font=font, fill='black')  # Для жирности
                elif int(info1PFO[0][0]) > int(message_arr[count_db_table + 1]):
                    if str(info1PFO[0][0]) != '-':
                        message_arr_output = message_arr[count_db_table + 1][:len(message_arr[count_db_table + 1]) - 3] + ' ' + message_arr[count_db_table + 1][len(message_arr[count_db_table + 1]) - 3:len(message_arr[count_db_table + 1])]
                        idraw.text((PosXPFO, PosYPFO), message_arr_output, font=font, fill='red')
                        idraw.text((PosXPFO + 1, PosYPFO), message_arr_output, font=font, fill='red')  # Для жирности
                        info0output = info1PFO[0][0][:len(info1PFO[0][0]) - 3] + ' ' + info1PFO[0][0][len(info1PFO[0][0]) - 3:len(info1PFO[0][0])]
                        idraw.text((PosXPFO, PosYPFO + 15), info0output, font=font, fill='black')
                    else:
                        message_arr_output = message_arr[count_db_table + 1][:len(message_arr[count_db_table + 1]) - 3] + ' ' + message_arr[count_db_table + 1][len(message_arr[count_db_table + 1]) - 3:len(message_arr[count_db_table + 1])]
                        idraw.text((PosXPFO, PosYPFO), message_arr_output, font=font, fill='black')
                        idraw.text((PosXPFO + 1, PosYPFO), message_arr_output, font=font, fill='black')  # Для жирности
            cur.execute('DROP TABLE line' + str(count))
            base.commit()
            base.execute('CREATE TABLE IF NOT EXISTS line' + str(count) + '(info0, info1)')
            base.commit()
            cur.execute('INSERT INTO line' + str(count) + ' VALUES(?, ?)', (message_arr[count_db_table], message_arr[count_db_table + 1]))
            base.commit()
            count += 1
            count_db_table += 2
        image.save('png/КартаИтог.png')
        image0 = open('png/КартаИтог.png', 'rb')
        await bot.send_photo(id, image0)

    # Создание ексель
    if str(message_arr[0]) == 'Ексель':
        if str(message_arr[1]) == 'Рынок':
            arr = ['Пшеница', 'Ячмень', 'Кукуруза', 'Горох', 'Соя', 'Подсолнечник', 'Рапс', 'Овес', 'Рожь']
            base = sqlite3.connect('db/PhotoRinok.db')
            cur = base.cursor()
            count = 0
            while count < len(arr):
                if str(message_arr[2]) == arr[count]:
                    name_line = count + 1
                count += 1
            info0 = cur.execute('SELECT date FROM DBlinePlot' + str(name_line)).fetchall()
            info1 = cur.execute('SELECT info0 FROM DBlinePlot' + str(name_line)).fetchall()
            info2 = cur.execute('SELECT info1 FROM DBlinePlot' + str(name_line)).fetchall()
            info_date = []
            count = 0
            while count < len(info0):
                info_date += [str(info0[count][0])]
                count += 1
            info_cfo = []
            count = 0
            while count < len(info1):
                info_cfo += [str(info1[count][0])]
                count += 1
            info_ufo = []
            count = 0
            while count < len(info2):
                info_ufo += [str(info2[count][0])]
                count += 1

            indexstart = info_date.index(message_arr[3])
            indexstop = info_date.index(message_arr[4])
            info_date = info_date[indexstart:indexstop + 1]
            info_cfo = info_cfo[indexstart:indexstop + 1]
            info_ufo = info_ufo[indexstart:indexstop + 1]
            base.execute('CREATE TABLE IF NOT EXISTS timedb(date, CFO, UFO)')
            base.commit()
            count = 0
            while count < len(info_date):
                cur.execute('INSERT INTO timedb VALUES(?, ?, ?)', (info_date[count], info_cfo[count], info_ufo[count]))
                base.commit()
                count += 1

            conn = sqlite3.connect(r'db/PhotoRinok.db')
            df = pd.read_sql('select * from timedb', conn)
            df.to_excel(r'data/Data.xlsx', index=False)
            info0 = cur.execute('SELECT date FROM timedb').fetchall()
            info1 = cur.execute('SELECT CFO FROM timedb').fetchall()
            info2 = cur.execute('SELECT UFO FROM timedb').fetchall()
            cur.execute('DROP TABLE timedb')
            base.commit()
            info_date = []
            count = 0
            while count < len(info0):
                info_date += [str(info0[count][0])]
                count += 1
            info_cfo = []
            count = 0
            while count < len(info1):
                info_cfo += [str(info1[count][0])]
                count += 1
            info_ufo = []
            count = 0
            while count < len(info2):
                info_ufo += [str(info2[count][0])]
                count += 1

            plt.axis([info_date[0], info_date[-1], 0, 50000])
            plt.title('Зависимость ЦФО')
            plt.xlabel('Дата')
            plt.ylabel('Значение ЦФО')
            plt.plot(info_date, info_cfo)
            plt.savefig('png/plotCFO.png')
            image = open('png/plotCFO.png', 'rb')
            await bot.send_photo(id, image)

            plt.axis([info_date[0], info_date[-1], 0, 50000])
            plt.title('Зависимость ЮФО')
            plt.xlabel('Дата')
            plt.ylabel('Значение ЮФО')
            plt.plot(info_date, info_ufo)
            plt.savefig('png/plotUFO.png')
            image = open('png/plotUFO.png', 'rb')
            await bot.send_photo(id, image)

            table_info = open(r'data/Data.xlsx', 'rb')
            await bot.send_document(id, table_info)

        if str(message_arr[1]) == 'Экспорт':
            arr = ['Пшеница', 'Ячмень', 'Горох', 'Кукуруза', 'Лен']
            base = sqlite3.connect('db/PhotoEksport.db')
            cur = base.cursor()
            count = 0
            while count < len(arr):
                if str(message_arr[2]) == arr[count]:
                    name_line = count + 1
                count += 1
            info0 = cur.execute('SELECT data FROM DBlinePlot' + str(name_line)).fetchall()
            info1 = cur.execute('SELECT city1 FROM DBlinePlot' + str(name_line)).fetchall()
            info2 = cur.execute('SELECT city2 FROM DBlinePlot' + str(name_line)).fetchall()
            info3 = cur.execute('SELECT city3 FROM DBlinePlot' + str(name_line)).fetchall()
            info4 = cur.execute('SELECT city4 FROM DBlinePlot' + str(name_line)).fetchall()
            info_date = []
            count = 0
            while count < len(info0):
                info_date += [str(info0[count][0])]
                count += 1
            info_city1 = []
            count = 0
            while count < len(info1):
                info_city1 += [str(info1[count][0])]
                count += 1
            info_city2 = []
            count = 0
            while count < len(info2):
                info_city2 += [str(info2[count][0])]
                count += 1
            info_city3 = []
            count = 0
            while count < len(info3):
                info_city3 += [str(info3[count][0])]
                count += 1
            info_city4 = []
            count = 0
            while count < len(info4):
                info_city4 += [str(info4[count][0])]
                count += 1

            indexstart = info_date.index(str(message_arr[3]))
            indexstop = info_date.index(str(message_arr[4]))

            info_date = info_date[indexstart:indexstop + 1]
            info_city1 = info_city1[indexstart:indexstop + 1]
            info_city2 = info_city2[indexstart:indexstop + 1]
            info_city3 = info_city3[indexstart:indexstop + 1]
            info_city4 = info_city4[indexstart:indexstop + 1]
            base.execute('CREATE TABLE IF NOT EXISTS timedb(data, city1, city2, city3, city4)')
            base.commit()
            count = 0
            while count < len(info_date):
                cur.execute('INSERT INTO timedb VALUES(?, ?, ?, ?, ?)', (info_date[count], info_city1[count], info_city2[count], info_city3[count], info_city4[count]))
                base.commit()
                count += 1

            conn = sqlite3.connect(r'db/PhotoEksport.db')
            df = pd.read_sql('select * from timedb', conn)
            df.to_excel(r'data/Data.xlsx', index=False)
            info0 = cur.execute('SELECT data FROM timedb').fetchall()
            info1 = cur.execute('SELECT city1 FROM timedb').fetchall()
            info2 = cur.execute('SELECT city2 FROM timedb').fetchall()
            info3 = cur.execute('SELECT city3 FROM timedb').fetchall()
            info4 = cur.execute('SELECT city4 FROM timedb').fetchall()
            cur.execute('DROP TABLE timedb')
            base.commit()
            info_date = []
            count = 0
            while count < len(info0):
                info_date += [str(info0[count][0])]
                count += 1
            info_city1 = []
            count = 0
            while count < len(info1):
                info_city1 += [str(info1[count][0])]
                count += 1
            info_city2 = []
            count = 0
            while count < len(info2):
                info_city2 += [str(info2[count][0])]
                count += 1
            info_city3 = []
            count = 0
            while count < len(info3):
                info_city3 += [str(info3[count][0])]
                count += 1
            info_city4 = []
            count = 0
            while count < len(info4):
                info_city4 += [str(info4[count][0])]
                count += 1

            plt.axis([info_date[0], info_date[-1], 0, 50000])
            plt.title('Зависимость для Новороссийска')
            plt.xlabel('Дата')
            plt.ylabel('Цена')
            plt.plot(info_date, info_city1)
            plt.savefig('png/plotNovoros.png')
            image = open('png/plotNovoros.png', 'rb')
            await bot.send_photo(id, image)

            plt.axis([info_date[0], info_date[-1], 0, 50000])
            plt.title('Зависимость для Тамани')
            plt.xlabel('Дата')
            plt.ylabel('Цена')
            plt.plot(info_date, info_city2)
            plt.savefig('png/plotTaman.png')
            image = open('png/plotTaman.png', 'rb')
            await bot.send_photo(id, image)

            plt.axis([info_date[0], info_date[-1], 0, 50000])
            plt.title('Зависимость для Азова')
            plt.xlabel('Дата')
            plt.ylabel('Цена')
            plt.plot(info_date, info_city3)
            plt.savefig('png/plotAzov.png')
            image = open('png/plotAzov.png', 'rb')
            await bot.send_photo(id, image)

            plt.axis([info_date[0], info_date[-1], 0, 50000])
            plt.title('Зависимость для Астрахани')
            plt.xlabel('Дата')
            plt.ylabel('Цена')
            plt.plot(info_date, info_city4)
            plt.savefig('png/plotAstraxan.png')
            image = open('png/plotAstraxan.png', 'rb')
            await bot.send_photo(id, image)

            table_info = open(r'data/Data.xlsx', 'rb')
            await bot.send_document(id, table_info)


executor.start_polling(db, skip_updates=True)

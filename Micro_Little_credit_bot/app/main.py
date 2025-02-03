from aiogram import F, Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from aiogram.utils.media_group import MediaGroupBuilder

import pandas as pd
import asyncio
import datetime

from config import TOKEN
from keyboards.keyboards import kb_approval, kb_pay_done, kb_finish, kb_file_done
from model import Form
import logging


logging.basicConfig(
    filename="error_log.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.ERROR,
    encoding="utf-8"
)

logger = logging.getLogger(__name__)

bot = Bot(TOKEN)
dp = Dispatcher()


async def post_exel(id, data):
    df_existing = pd.read_excel('media/data.xlsx')
    new_data = [[
        id,
        data.get("name"),
        data.get("get_phone_number"),
        data.get("approval"),
        datetime.datetime.now()
    ]]
    
    filtered_data = df_existing.loc[df_existing['ID'] == id]
    if not filtered_data.empty:
        is_approval = filtered_data['БЫЛО ЛИ СОГЛАСИЕ'].values[0]
        if data.get("approval") == "Согласен" and is_approval == "Нет":
            is_approval = "Да"
        new_data[0].append(is_approval)
        if data.get("approval") == "Согласен":
            count_approval = int(filtered_data['СКОЛЬКО РАЗ СОГЛАСИЕ'].values[0]) + 1
        else:
            count_approval = int(filtered_data['СКОЛЬКО РАЗ СОГЛАСИЕ'].values[0]) + 0
        new_data[0].append(count_approval)
    else:
        if data.get("approval") == "Согласен": 
            new_data[0].append("Да")
            new_data[0].append(1)
        if data.get("approval") == "Отказ": 
            new_data[0].append("Нет")
            new_data[0].append(0)
            
    df_new = pd.DataFrame(new_data, columns=df_existing.columns)
    df_updated = pd.concat([df_existing, df_new]).drop_duplicates(subset=["ID"], keep="last")
    df_updated.to_excel('media/data.xlsx', index=False, engine='openpyxl')
    return True


@dp.message(Command('export'))
async def start(message: Message, state: FSMContext):
    try:
        if int(message.from_user.id) in [7530798787, 689331353]:
            await bot.send_document(message.chat.id, document=FSInputFile("media/data.xlsx"))
            await state.clear()
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'export'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    try:
        await message.answer('Введите ваше имя:', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.name)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'start'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


@dp.message(F.text, Form.name)
async def name(message: Message, state: FSMContext):
    try:
        await state.update_data(name=message.text)
        await message.answer('Введите ваш номер телефона:', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.get_phone_number)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'name'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


@dp.message(F.text, Form.get_phone_number)
async def get_phone_number(message: Message, state: FSMContext):
    try:
        await state.update_data(get_phone_number=message.text)
        await message.answer_document(document=FSInputFile('media/Договор офферты.docx'))
        await message.answer_document(document=FSInputFile('media/Обработка персональных данных.docx'))
        await message.answer("Нажимая кнопку *Согласиться* - я даю свое согласие на обработку персональных данных и оказание платных консультационных услуг в соответствии с прикрепленными выше документами. Мне известны условия и стоимость консультации. *Стоимость консультации 2000 рублей.*\n\n\nПодробная информация об услуге размещена на сайте:\nhttps://ystroim-vsekh.ru\n\n(Нажмите кнопоку в всплывающем меню)", reply_markup=kb_approval, parse_mode="Markdown")
        await state.set_state(Form.approval)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'phone_number'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


@dp.message(F.text, Form.approval)
async def approval(message: Message, state: FSMContext):
    try:
        if message.text == "✅Согласиться":
            await state.update_data(approval="Согласен")
            await message.answer("Для проведения консультации *необходимо* произвести оплату.\n\nНиже прикреплен QR-код для оплаты:", reply_markup=kb_pay_done, parse_mode="Markdown")
            await message.answer_photo(photo=FSInputFile('media/qr.png'))
            await state.set_state(Form.pay_done)
        if message.text == "❌Отказаться":
            await state.update_data(approval="Отказ")
            await message.answer("Вы отказались от консультации. Спасибо, что воспользовались нашим ботом!", reply_markup=ReplyKeyboardRemove())     
            
            data = await state.get_data()
            response = await post_exel(message.from_user.id, data)
            await state.clear()
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'approval'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


@dp.message(F.text, Form.pay_done)
async def approval(message: Message, state: FSMContext):
    try:
        if message.text == "✅Консультацию оплатил":
            await message.answer("*Для полного анализа вашей ситуации* необходимо сформировать файл кредитной истории.\n\nДля этого *нужно перейти на сайт*:\nhttps://credistory.ru\n\nИ *следовать инструкции* представленной ниже⬇️", reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")
            
            media = MediaGroupBuilder()
            media.add_photo(media=FSInputFile("media/credit_history_first.jpg"), caption='❗️*Пошаговая инструкция* как скачать файл кредитной истории', parse_mode="Markdown")
            media.add_photo(media=FSInputFile("media/credit_history_second.jpg"))
            await message.answer_media_group(media=media.build())
            
            await message.answer("Вы уже *подготовили необходимый файл* и *оплатили услугу*?", reply_markup=kb_file_done, parse_mode="Markdown")
            await state.set_state(Form.credit_history_done)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'approval'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


@dp.message(F.text, Form.credit_history_done)
async def pay_done(message: Message, state: FSMContext):
    try:
        if message.text == "✅Все верно":
            await message.answer("После оплаты - *отправьте сформированый файл нашему менеджеру*: @odobrim\_vsekh\n\nДалее наш специалист свяжется с Вами для консультации!", reply_markup=kb_finish, parse_mode="Markdown")
            await state.set_state(Form.finish)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'pay_done'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


@dp.message(F.text, Form.finish)  
async def finish(message: Message, state: FSMContext):
    try:
        if message.text == "✅Отправил": 
            await message.answer_photo(photo=FSInputFile('media/last_message_photo.jpg'), caption="Спасибо, что воспользовались нашим ботом!\nВ ближайшее время *наш менеджер Вам позвонит*.\nУспехов в одобрении!\n\nИнформацию по другим услугам можете узнать на нашем сайте или в профиле компании в яндексе:\n\n*Сайт*:\nhttps://ystroim-vseh.clients.site/\n\n*Наша компания в яндексе*:\nhttps://yandex.ru/profile/13064319362\n\n*Дополнительный сайт*:\nhttps://ystroim-vsekh.ru/", reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")
            
            data = await state.get_data()
            response = await post_exel(message.from_user.id, data)
            await state.clear()
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'finish'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

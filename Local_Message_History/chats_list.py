# from pyrogram import Client
# import configparser
# import sys
# sys.path.append("PLIB")


# config = configparser.ConfigParser()
# config.read("settings.ini")

# api_hash = config["CONFIG"]["api_hash"]
# api_id = config["CONFIG"]["api_id"]


# # 3-й Спринт
# # 1) Сделать новую функцию py, начитка списка групп,чатов в txt файл  (Id <tab> название <tab> тип(чат,группа, канал,супер-группа, избраное))


# with Client(name="my_account", api_hash=api_hash, api_id=api_id) as app:
#     count = 1
#     file = open('chats_list.txt', 'w', encoding="utf-8")
#     for dialog in app.get_dialogs():
#         chat_info = dialog.chat
#         file.write(f"{count}. {chat_info.id}      {chat_info.title if chat_info.title else chat_info.first_name}      {chat_info.type}\n")
#         print(f"{count}. {chat_info.id}      {chat_info.title if chat_info.title else chat_info.first_name}      {chat_info.type}\n")
#     file.close()






import re

from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile

from keyboards.user import (
    kb_yn, kb_2, kb_3, kb_4,
    kb_back, kb_check_data,
    kb_approval, kb_phone_number)
from states.user import Form
from services.service import Service
from handlers.manager import start_mailing_to_managers


user_router = Router()


@user_router.message(F.text, Form.name)
async def state_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите ваш номер телефона', reply_markup=kb_phone_number)
    await state.set_state(Form.phone_number)


@user_router.message(F.text, Form.phone_number)
async def state_region(message: Message, state: FSMContext):
    if message.text == "🔙Назад":
        await message.answer('Введите ваше имя:', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.name)
    else:
        if message.text == "Пропустить":
             await state.update_data(phone_number="Не указан")
        else:
            await state.update_data(phone_number=message.text)
        await message.answer('Регион, где планируете взять потребительский кредит/ипотеку?\n\n(Напишите ответ)', reply_markup=kb_back)
        await state.set_state(Form.region)

    
@user_router.message(F.text, Form.region)
async def state_region(message: Message, state: FSMContext):
    if message.text == "🔙Назад":
        await message.answer('Введите ваш номер телефона', reply_markup=kb_phone_number)
        await state.set_state(Form.phone_number)
    else:
        await state.update_data(region=message.text)
        await message.answer('Есть ли у вас судимость?\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_yn)
        await state.set_state(Form.criminal_record)


@user_router.message(F.text, Form.criminal_record)
async def state_criminal_record(message: Message, state: FSMContext):
    if message.text == "🔙Назад":
        await message.answer('Регион, где планируете взять потребительский кредит/ипотеку?\n\n(Напишите ответ)', reply_markup=kb_back)
        await state.set_state(Form.region)
    else:    
        await state.update_data(criminal_record=message.text)
        if message.text == "❌Нет":
            await state.update_data(is_criminal_record="")
            await state.update_data(end_of_the_criminal_record="")
            await state.update_data(is_economic_criminal_record="")
            await message.answer('Есть ли у вас исполнительное производство?\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_yn)
            await state.set_state(Form.is_enforcement_proceedings)
        elif message.text == "✅Да":
            await message.answer('Судимость погашена?\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_yn)
            await state.set_state(Form.is_criminal_record)
        
# --------------------------------------------------------
@user_router.message(F.text, Form.is_criminal_record)
async def state_is_criminal_record(message: Message, state: FSMContext):
    if message.text == "🔙Назад":
        await message.answer('Есть ли у вас судимость?\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_yn)
        await state.set_state(Form.criminal_record)
    else:    
        await state.update_data(is_criminal_record=message.text)
        if message.text == "❌Нет":
            await state.update_data(end_of_the_criminal_record="")
            await state.update_data(is_economic_criminal_record="")
            await message.answer('Есть ли у вас исполнительное производство?\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_yn)
            await state.set_state(Form.is_enforcement_proceedings)
        elif message.text == "✅Да":
            await message.answer('В каком году она была погашена?\n\n(Напишите ответ)', reply_markup=kb_back)
            await state.set_state(Form.end_of_the_criminal_record)


@user_router.message(F.text, Form.end_of_the_criminal_record)
async def state_end_of_the_criminal_record(message: Message, state: FSMContext):
    if message.text == "🔙Назад":
        await message.answer('Есть ли у вас судимость?\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_yn)
        await state.set_state(Form.criminal_record)
    else:
        tmp = re.findall(r'\d+', message.text)
        if tmp:
            await state.update_data(end_of_the_criminal_record=tmp[0])
            await message.answer('Статья по экономическим преступлениям?\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_yn)
            await state.set_state(Form.is_economic_criminal_record)
        else:
            await message.answer('Некорректное значение, введите год числом!', reply_markup=kb_back)


@user_router.message(F.text, Form.is_economic_criminal_record)
async def state_is_economic_criminal_record(message: Message, state: FSMContext):
    if message.text == "🔙Назад":
        await message.answer('Есть ли у вас судимость?\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_yn)
        await state.set_state(Form.criminal_record)
    else:
        if message.text == "✅Да" or message.text == "❌Нет":
            await state.update_data(is_economic_criminal_record=message.text)
            await message.answer('Есть ли у вас исполнительное производство?\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_yn)
            await state.set_state(Form.is_enforcement_proceedings)


@user_router.message(F.text, Form.is_enforcement_proceedings)
async def state_is_enforcement_proceedings(message: Message, state: FSMContext):
    if message.text == "🔙Назад":
        await message.answer('Есть ли у вас судимость?\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_yn)
        await state.set_state(Form.criminal_record)
    else:
        if message.text == "✅Да" or message.text == "❌Нет":
            await state.update_data(is_enforcement_proceedings=message.text)
            await message.answer('Какая у вас официальная заработная плата (... руб/мес)?\n\n(Напишите ответ)', reply_markup=kb_back)
            await state.set_state(Form.salary)


@user_router.message(F.text, Form.salary)
async def state_salary(message: Message, state: FSMContext):
    if message.text == "🔙Назад":
        await message.answer('Есть ли у вас исполнительное производство?\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_yn)
        await state.set_state(Form.is_enforcement_proceedings)
    else:
        salary_arr_int = re.findall(r'\d+', message.text)
        if salary_arr_int:

            salary_int = ""
            for x in salary_arr_int:
                salary_int += x
            await state.update_data(salary=salary_int)
            await message.answer('Являетесь ли вы зарплатником какого-либо банка?\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_2)
            await state.set_state(Form.is_bank_salary_employee)
        else:
            await message.answer('Некорректное значение, введите заработную плату числом!', reply_markup=kb_back)


@user_router.message(F.text, Form.is_bank_salary_employee)
async def state_is_bank_salary_employee(message: Message, state: FSMContext):
    if message.text == "🔙Назад":
        await message.answer('Какая у вас официальная заработная плата (... руб/мес)?\n\n(Напишите ответ)', reply_markup=kb_back)
        await state.set_state(Form.salary)
    else:
        if message.text == "✅Да" or message.text == "❌Нет" or message.text == "Пропустить":
            if message.text == "Пропустить":
                await state.update_data(is_bank_salary_employee="Не указано")
            else:
                await state.update_data(is_bank_salary_employee=message.text)
            await message.answer('Сколько вам полных лет?', reply_markup=kb_back)
            await state.set_state(Form.age)


@user_router.message(F.text, Form.age)
async def state_age(message: Message, state: FSMContext):
    if message.text == "🔙Назад":
        await message.answer('Являетесь ли вы зарплатником какого-либо банка?\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_2)
        await state.set_state(Form.is_bank_salary_employee)
    else:
        tmp = re.findall(r'\d+', message.text)
        if tmp:
            await state.update_data(age=tmp[0])
            await message.answer('Ранее уже брали кредит/ипотеку?\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_yn)
            await state.set_state(Form.is_credit_earlier)
        else:
            await message.answer('Некорректное значение, введите возраст числом!', reply_markup=kb_back)


@user_router.message(F.text, Form.is_credit_earlier)
async def state_is_credit_earlier(message: Message, state: FSMContext):
    if message.text == "🔙Назад":
        await message.answer('Сколько вам полных лет?', reply_markup=kb_back)
        await state.set_state(Form.age)
    else:
        if message.text == "✅Да" or message.text == "❌Нет":
            await state.update_data(is_credit_earlier=message.text)
            if message.text == "❌Нет":
                await message.answer('Был ли отказ в выдаче кредита/ипотеки?\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_yn)
                await state.set_state(Form.is_credit_earlier_fail)
            if message.text == "✅Да":
                await message.answer('Какой вид кредита планируете взять - потребительский/ипотека?\n\n(Напишите вид словами, потребительский или ипотека. Мы поймем)', reply_markup=ReplyKeyboardRemove())
                await state.set_state(Form.credit_type)


@user_router.message(F.text, Form.is_credit_earlier_fail)
async def state_is_credit_earlier_fail(message: Message, state: FSMContext):
    if message.text == "🔙Назад":
        await message.answer('Ранее уже брали кредит/ипотеку?\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_yn)
        await state.set_state(Form.is_credit_earlier)
    else:
        if message.text == "✅Да" or message.text == "❌Нет":
            await state.update_data(is_credit_earlier_fail=message.text)
            await message.answer('Какой вид кредита планируете взять - потребительский/ипотека?\n\n(Напишите вид словами, потребительский или ипотека. Мы поймем)', reply_markup=kb_back)
            await state.set_state(Form.credit_type)


@user_router.message(F.text, Form.credit_type)
async def state_credit_type(message: Message, state: FSMContext):
    if message.text == "🔙Назад":
        await message.answer('Ранее уже брали кредит/ипотеку?\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_yn)
        await state.set_state(Form.is_credit_earlier)
    else:
        await state.update_data(credit_type=message.text)
        username = message.from_user.username
        if username == "None":
            await message.answer('Не смогли получить ваш тег для дальнейшей связи. Без этого дальнейшая работа невозможна. Установите себе никнейм и пришлите его в чат. Или пришлите ссылку на ваш аккаунт:', reply_markup=kb_back)
            await state.set_state(Form.username)
        else:
            await state.update_data(username=f'@{username}')
            data = await state.get_data()
            if data.get("phone_number") == "Не указан":
                await message.answer('Рекомендуем оставить свой номер телефона, так наш менеджер быстрее с вами свяжется и поможет в вашем вопросе:', reply_markup=kb_phone_number)
                await state.set_state(Form.repeat_phone_number)
            else:
                mes = f'Пожалуйста, проверьте все ли верно:\n' + \
                        f'- Ваше имя: {data.get("name")}\n' + \
                        f'- Регион, где планируете взять кредит: {data.get("region")}\n' + \
                        f'- Есть ли у вас судимость: {data.get("criminal_record")}\n'
                if data.get("criminal_record") == "✅Да":
                    mes += f'- Судимость погашена: {data.get("is_criminal_record")}\n'
                    if data.get("is_criminal_record") == "✅Да":
                        mes += f'- Судимость погашена в {data.get("end_of_the_criminal_record")}\n'       
                        mes += f'- Статья по экономическим преступлениям: {data.get("is_economic_criminal_record")}\n'
                mes += f'- Есть ли у вас исполнительное производство: {data.get("is_enforcement_proceedings")}\n' + \
                        f'- Ваша официальная зарплата: {data.get("salary")} руб/мес.\n' + \
                        f'- Являетесь ли вы зарплатником какого-либо банка: {data.get("is_bank_salary_employee")}\n' + \
                        f'- Ваш возраст: {data.get("age")} лет\n' + \
                        f'- Раньше уже брали кредит/ипотеку: {data.get("is_credit_earlier")}\n'
                if data.get("is_credit_earlier") == "❌Нет":
                    mes += f'- Был ли отказ в выдаче кредита/ипотеки: {data.get("is_credit_earlier_fail")}\n'
                mes += f'- Планируемый вид кредита: {data.get("credit_type")}\n' + \
                        f'- Ваш телеграм: {data.get("username")}\n' + \
                        f'- Ваш телефон: {data.get("phone_number")}\n' + \
                        f'(Нажмите одну из кнопок в всплывающем меню)'
                await message.answer(mes, reply_markup=kb_check_data)
                await state.set_state(Form.check_state)


@user_router.message(F.text, Form.username)
async def state_username(message: Message, state: FSMContext):
    if message.text == "🔙Назад":
        await message.answer('Какой вид кредита планируете взять - потребительский/ипотека?\n\n(Напишите вид словами, потребительский или ипотека. Мы поймем)', reply_markup=kb_back)
        await state.set_state(Form.credit_type)
    else:
        await state.update_data(username=message.text)
        data = await state.get_data()
        if data.get("phone_number") == "Не указан":
            await message.answer('Рекомендуем оставить свой номер телефона, так наш менеджер быстрее с вами свяжется и поможет в вашем вопросе:', reply_markup=kb_phone_number)
            await state.set_state(Form.repeat_phone_number)
        else:
            mes = f'Пожалуйста, проверьте все ли верно:\n' + \
                    f'- Ваше имя: {data.get("name")}\n' + \
                    f'- Регион, где планируете взять кредит: {data.get("region")}\n' + \
                    f'- Есть ли у вас судимость: {data.get("criminal_record")}\n'
            if data.get("criminal_record") == "✅Да":
                mes += f'- Судимость погашена: {data.get("is_criminal_record")}\n'
                if data.get("is_criminal_record") == "✅Да":
                    mes += f'- Судимость погашена в {data.get("end_of_the_criminal_record")}\n'       
                    mes += f'- Статья по экономическим преступлениям: {data.get("is_economic_criminal_record")}\n'
            mes += f'- Есть ли у вас исполнительное производство: {data.get("is_enforcement_proceedings")}\n' + \
                    f'- Ваша официальная зарплата: {data.get("salary")} руб/мес.\n' + \
                    f'- Являетесь ли вы зарплатником какого-либо банка: {data.get("is_bank_salary_employee")}\n' + \
                    f'- Ваш возраст: {data.get("age")} лет\n' + \
                    f'- Раньше уже брали кредит/ипотеку: {data.get("is_credit_earlier")}\n'
            if data.get("is_credit_earlier") == "❌Нет":
                mes += f'- Был ли отказ в выдаче кредита/ипотеки: {data.get("is_credit_earlier_fail")}\n'
            mes += f'- Планируемый вид кредита: {data.get("credit_type")}\n' + \
                    f'- Ваш телеграм: {data.get("username")}\n' + \
                    f'- Ваш телефон: {data.get("phone_number")}\n' + \
                    f'(Нажмите одну из кнопок в всплывающем меню)'
            await message.answer(mes, reply_markup=kb_check_data)
            await state.set_state(Form.check_state)


@user_router.message(F.text, Form.repeat_phone_number)
async def state_phone_number(message: Message, state: FSMContext):
    if message.text == "🔙Назад":
        username = message.from_user.username
        if username == "None":
            await message.answer('Не смогли получить ваш тег для дальнейшей связи. Без этого дальнейшая работа невозможна. Установите себе никнейм и пришлите его в чат. Или пришлите ссылку на ваш аккаунт:', reply_markup=kb_back)
            await state.set_state(Form.username)
        else:
            await message.answer('Какой вид кредита планируете взять - потребительский/ипотека?\n\n(Напишите вид словами, потребительский или ипотека. Мы поймем)', reply_markup=kb_back)
            await state.set_state(Form.credit_type)
    else:
        if message.text == "Пропустить":
            await state.update_data(phone_number="Не указан")
        else:
            await state.update_data(phone_number=message.text)

        # Вывод всей информации о пользователю ему самому для проверки
        data = await state.get_data()
        mes = f'Пожалуйста, проверьте все ли верно:\n' + \
                f'- Ваше имя: {data.get("name")}\n' + \
                f'- Регион, где планируете взять кредит: {data.get("region")}\n' + \
                f'- Есть ли у вас судимость: {data.get("criminal_record")}\n'
        if data.get("criminal_record") == "✅Да":
            mes += f'- Судимость погашена: {data.get("is_criminal_record")}\n'
            if data.get("is_criminal_record") == "✅Да":
                mes += f'- Судимость погашена в {data.get("end_of_the_criminal_record")}\n'       
                mes += f'- Статья по экономическим преступлениям: {data.get("is_economic_criminal_record")}\n'
        mes += f'- Есть ли у вас исполнительное производство: {data.get("is_enforcement_proceedings")}\n' + \
                f'- Ваша официальная зарплата: {data.get("salary")} руб/мес.\n' + \
                f'- Являетесь ли вы зарплатником какого-либо банка: {data.get("is_bank_salary_employee")}\n' + \
                f'- Ваш возраст: {data.get("age")} лет\n' + \
                f'- Раньше уже брали кредит/ипотеку: {data.get("is_credit_earlier")}\n'
        if data.get("is_credit_earlier") == "❌Нет":
            mes += f'- Был ли отказ в выдаче кредита/ипотеки: {data.get("is_credit_earlier_fail")}\n'
        mes += f'- Планируемый вид кредита: {data.get("credit_type")}\n' + \
                f'- Ваш телеграм: {data.get("username")}\n' + \
                f'- Ваш телефон: {data.get("phone_number")}\n' + \
                f'(Нажмите одну из кнопок в всплывающем меню)'
        await message.answer(mes, reply_markup=kb_check_data)
        await state.set_state(Form.check_state)


@user_router.message(F.text, Form.check_state)
async def state_check_state(message: Message, state: FSMContext):
    if message.text == "🔙Назад":
        await message.answer('Рекомендуем оставить свой номер телефона, так наш менеджер быстрее с вами свяжется и поможет в вашем вопросе:', reply_markup=kb_phone_number)
        await state.set_state(Form.phone_number)
    if message.text == "❌Заполнить заново":
        await message.answer('Запускаем заполнение анкеты с начала. \n\nВведите ваше имя:', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.name)
    if message.text == "✅Все верно":   
        user_id = message.from_user.id

        if not await Service.user.get_user_info(user_id=user_id):
            data = await state.get_data()
        else:
            data = await Service.user.get_user_info(user_id=user_id)

        # Эта переменная с информацией из анкеты передается в БД
        user_data = {
            'user_id': user_id,
            'name': data.get("name"),
            'region': data.get("region"),
            'criminal_record': data.get("criminal_record"),
            'is_criminal_record': data.get("is_criminal_record"),
            'end_of_the_criminal_record': data.get("end_of_the_criminal_record"),
            'is_economic_criminal_record': data.get("is_economic_criminal_record"),
            'is_enforcement_proceedings': data.get("is_enforcement_proceedings"),
            'salary': data.get("salary"),
            'is_bank_salary_employee': data.get("is_bank_salary_employee"),
            'age': data.get("age"),
            'is_credit_earlier': data.get("is_credit_earlier"),
            'is_credit_earlier_fail': data.get("is_credit_earlier_fail"),
            'credit_type': data.get("credit_type"),
            'username': data.get("username"),
            'phone_number': data.get("phone_number"),
            'completed': False,
            'number_completed': 0,
            'number_changes': 0,
            'date_last_change': datetime.now().date(),
        }

        if (data.get("criminal_record") == "❌Нет" and data.get("is_enforcement_proceedings") == "❌Нет" and int(data.get("salary")) > 85000 and 25 < int(data.get("age")) < 45):
            mes = 'Спасибо за прохождение анкеты! Предварительно введенные вами параметры удовлетворяют скоринговым моделям банка:\n' + \
                  '- Нет судимости\n' + \
                  '- Нет исполнительного производства\n' + \
                  '- Официальная заработная плата может соответствовать финансовой нагрузке\n'
            if data.get("is_bank_salary_employee") == "✅Да":
                mes += f'- Являетесь зарплатником банка\n'
            mes += '- Попадаете в возрастной диапазон, который соответствует меньшему проценту дефолтности\n' + \
                   'А значит - есть шанс получить одобрение.\n\n' + \
                   'Однако для точного ответа этого недостаточно, так как необходимо проанализировать и другие параметры, которых намного больше\n\n' + \
                   'В ближайшее время наш менеджер свяжется с вами для уточнения деталей. (Звонок менеджера абсолютно бесплатный).\n\n' + \
                  f'Телефон для связи: {data.get("phone_number")}\nТелеграм: {data.get("username")}\n\n' + \
                   'И, при вашем согласии, менеджер проведет консультацию по вашему вопросу. А так же, ПОЛНЫЙ финансово-экономический анализ.\n(Стоимость консультации 2000 руб., длительность до 25 минут)'
            await message.answer(mes, reply_markup=ReplyKeyboardRemove()) 
            
            user_data['important_user'] = True
            await Service.user.create_or_update_user(user_data=user_data)
            await start_mailing_to_managers(message)

        else:
            mes = 'Спасибо за прохождение анкеты! Предварительно некоторые введенные вами параметры удовлетворяют скоринговым моделям банка:\n'
            if data.get("criminal_record") == "❌Нет":
                mes += '- Нет судимости\n'
            if data.get("is_enforcement_proceedings") == "❌Нет":
                mes += '- Нет исполнительного производства\n'
            if int(data.get("salary")) > 85000:
                mes += '- Официальная заработная плата может соответствовать финансовой нагрузке\n'
            if data.get("is_bank_salary_employee") == "✅Да":
                mes += '- Являетесь зарплатником банка\n'
            if 25 < int(data.get("age")) < 45:
                mes += '- Попадаете в возрастной диапазон, который соответствует меньшему проценту дефолтности\n'

            mes += 'Но у вас:\n'
            if not 25 < int(data.get("age")) < 45:
                mes += '- Не попадаете в возрастной диапазон, который соответствует меньшему проценту дефолтности\n'
            if data.get("is_criminal_record") == "✅Да":
                mes += '- Есть действующая судимость\n'
            if data.get("is_enforcement_proceedings") == "✅Да":
                mes += '- Есть исполнительное производство\n'

            if data.get("is_criminal_record") == "❌Нет":
                if data.get("is_economic_criminal_record") == "✅Да":
                    mes += '- Была судимость по экономическим статьям\n'
                else:
                    if int(datetime.now().year) - int(data.get("end_of_the_criminal_record")) <= 5:
                        mes += '- Есть недавно погашенная судимость - поэтому скоринговый у вас балл будет низким\n'
                    if int(datetime.now().year) - int(data.get("end_of_the_criminal_record")) > 5:
                        mes += f'- Есть погашенная судимость {int(datetime.now().year) - int(data.get("end_of_the_criminal_record"))} лет назад, если за это время вы не брали кредиты - скоринговый балл будет низким\n'
            
            if int(data.get("salary")) <= 85000:
                mes += '- Официальная заработная плата может не соответствовать финансовой нагрузке\n'
            if data.get("is_bank_salary_employee") == "❌Нет" or data.get("is_bank_salary_employee") == "Не указано":
                mes += '- Вы не являетесь зарплатником банка\n'
            if int(data.get("salary")) < 25 and int(data.get("salary")) > 45:
                mes += '- Вы не попадаете в возрастной диапазон, который соответствует меньшему проценту дефолтности\n'
            
            mes += 'А значит, есть вероятность отказа вашей заявки.\n\n' + \
                   'Однако для точного ответа этого недостаточно, так как необходимо проанализировать и другие параметры, которых намного больше.\n\n' + \
                   'В ближайшее время наш менеджер свяжется с вами для уточнения деталей. (Звонок менеджера абсолютно бесплатный).\n\n' + \
                  f'Телефон для связи: {data.get("phone_number")}\nТелеграм: {data.get("username")}\n\n' + \
                   'И, при вашем согласии, менеджер проведет консультацию по вашему вопросу. А так же, ПОЛНЫЙ финансово-экономический анализ.\n(Стоимость консультации 2000 руб., длительность до 25 минут)'
            await message.answer(mes, reply_markup=ReplyKeyboardRemove())
            
            user_data['important_user'] = False

            await Service.user.create_or_update_user(user_data=user_data)

        # Переходим к оценке бота
        await message.answer('Оцените, пожалуйста, работу бота\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_3)
        await state.set_state(Form.mark)
    

@user_router.message(F.text, Form.mark)
async def state_mark(message: Message, state: FSMContext):
    if message.text == "Понравилось" or message.text == "Не понравилось":
        await state.update_data(mark=message.text)
        await message.answer('При желании - можете написать ваши рекомендации (что можно улучшить в работе нашего бота):\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_4)
        await state.set_state(Form.is_feedback)


@user_router.message(F.text, Form.is_feedback)
async def state_is_feedback(message: Message, state: FSMContext):
    if message.text == "Оставить отзыв" or message.text == "Пропустить":
        await state.update_data(is_feedback=message.text)
        if message.text == "Оставить отзыв":
            await message.answer('Напишите ваш отзыв:', reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.feedback) 
        if message.text == "Пропустить":   
            await state.update_data(feedback="Не указан")
            data = await state.get_data()

            user_id = message.from_user.id
            mark = data.get("mark")
            feedback = data.get("feedback")

            await Service.user.save_feedback(user_id=user_id, mark=mark, feedback_text=feedback)

            await message.answer('Спасибо, что воспользовались нашим ботом!\nУспехов в одобрении!', reply_markup=ReplyKeyboardRemove())
            await message.answer('Но это еще не все, ожидайте сообщение!', reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.approval)


@user_router.message(F.text, Form.feedback)
async def state_feedback(message: Message, state: FSMContext):
    await state.update_data(feedback=message.text)
    data = await state.get_data()
    
    user_id = message.from_user.id
    mark = data.get("mark")
    feedback = data.get("feedback")

    await Service.user.save_feedback(user_id=user_id, mark=mark, feedback_text=feedback)
    
    await message.answer('Спасибо, что воспользовались нашим ботом!\nУспехов в одобрении!', reply_markup=ReplyKeyboardRemove())
    await message.answer('Но это еще не все, ожидайте сообщение!', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.approval)


@user_router.message(F.text, Form.approval)
async def state_approval(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text == 'Согласиться':
        await state.update_data(approval='Согласен')
        await message.answer('Ниже прикреплен qr-код для оплаты:', reply_markup=ReplyKeyboardRemove())
        await message.answer_photo(photo=FSInputFile(r"static\qr.png"),)
        await message.answer('Ниже прикреплен файл инструкции. Нажмите на него, откройте у себя на телефоне и следуйте алгоритму.\n\n(Ссылка на сайт: https://credistory.ru/)', reply_markup=ReplyKeyboardRemove())
        await message.answer_document(document=FSInputFile(r"static\Proverka_kredita.pdf"),)
        await Service.user.save_approval(user_id=user_id, approval=approval)

        await message.answer('Если вы еще не оставили отзыв или хотите дополнить имеющийся, просим вас это сделать. Ждем обратную связь!\n\n(Нажмите одну из кнопок в всплывающем меню)', reply_markup=kb_4)
        await state.set_state(Form.repeat_is_feedback)
    if message.text == 'Отказаться': 
        await state.update_data(approval='Не согласен')
        await message.answer('Без вашего согласия дальнейшяя работа недоступна. Для продолжения необходимо согласиться с предыдущими положениями', reply_markup=kb_approval)
        await Service.user.save_approval(user_id=user_id, approval=approval)
        await state.set_state(Form.approval)


@user_router.message(F.text, Form.repeat_is_feedback)
async def state_repeat_is_feedback(message: Message, state: FSMContext):
    if message.text == "Оставить отзыв" or message.text == "Пропустить":
        await state.update_data(repeat_is_feedback=message.text)
        if message.text == "Оставить отзыв":
            await message.answer('Напишите ваш отзыв:', reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.repeat_feedback)
        if message.text == "Пропустить":
            await state.update_data(repeat_feedback="Не указан")

            user_id = message.from_user.id
            repeat_feedback = "Не указан"

            await Service.user.save_repeat_feedback(user_id=user_id, repeat_feedback_text=repeat_feedback)

            await message.answer('Спасибо, что воспользовались нашим ботом!', reply_markup=ReplyKeyboardRemove())

            await state.clear()
            await state.set_state(Form.approval)


@user_router.message(F.text, Form.repeat_feedback)
async def state_repeat_feedback(message: Message, state: FSMContext):
    await state.update_data(feedback=message.text)
    data = await state.get_data()

    user_id = message.from_user.id
    repeat_feedback = data.get("repeat_feedback")

    await Service.user.save_repeat_feedback(user_id=user_id, repeat_feedback_text=repeat_feedback)

    await message.answer('Спасибо, что воспользовались нашим ботом!', reply_markup=ReplyKeyboardRemove())
    await state.clear()




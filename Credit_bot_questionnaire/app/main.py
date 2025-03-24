from aiogram import F, Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

import asyncio
import logging
import re

from app.resource.text import description_credit, allowable_credit_time
from app.keyboards.keyboards import kb_yn
# Импорт роутеров
from app.handlers.car_loan import car_loan_router
from app.handlers.credit_pod_zalog import credit_pod_zalog_router
from app.handlers.ipoteka import ipoteka_router
# from app.handlers.main import main_router
from app.handlers.micro_loan import micro_loan_router
# Импорт форм для всех модулей
from app.model import model_car_loan, model_credit_pod_zalog, model_ipoteka, model_main, model_microloan
# Импорт токена
from app.config import TOKEN

logging.basicConfig(
    filename="error_log.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.ERROR,
    encoding="utf-8"
)
logger = logging.getLogger(__name__)


dp = Dispatcher()
dp.include_routers(
    car_loan_router,
    credit_pod_zalog_router, 
    ipoteka_router
)


async def main():
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


# async def post_exel(id, data):
#     df_existing = pd.read_excel('media/data.xlsx')
#     new_data = [[
#         id,
#         data.get("name"),
#         data.get("get_phone_number"),
#         data.get("approval"),
#         datetime.datetime.now()
#     ]]
    
#     filtered_data = df_existing.loc[df_existing['ID'] == id]
#     if not filtered_data.empty:
#         is_approval = filtered_data['БЫЛО ЛИ СОГЛАСИЕ'].values[0]
#         if data.get("approval") == "Согласен" and is_approval == "Нет":
#             is_approval = "Да"
#         new_data[0].append(is_approval)
#         if data.get("approval") == "Согласен":
#             count_approval = int(filtered_data['СКОЛЬКО РАЗ СОГЛАСИЕ'].values[0]) + 1
#         else:
#             count_approval = int(filtered_data['СКОЛЬКО РАЗ СОГЛАСИЕ'].values[0]) + 0
#         new_data[0].append(count_approval)
#     else:
#         if data.get("approval") == "Согласен": 
#             new_data[0].append("Да")
#             new_data[0].append(1)
#         if data.get("approval") == "Отказ": 
#             new_data[0].append("Нет")
#             new_data[0].append(0)
            
#     df_new = pd.DataFrame(new_data, columns=df_existing.columns)
#     df_updated = pd.concat([df_existing, df_new]).drop_duplicates(subset=["ID"], keep="last")
#     df_updated.to_excel('media/data.xlsx', index=False, engine='openpyxl')
#     return True


# @dp.message(Command('export'))
# async def start(message: Message, state: FSMContext):
#     try:
#         if int(message.from_user.id) in [7530798787, 689331353]:
#             await bot.send_document(message.chat.id, document=FSInputFile("media/data.xlsx"))
#             await state.clear()
#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'export'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


@dp.message(CommandStart())
# Вопрос №1 - Вид кредита
async def start(message: Message, state: FSMContext):
    try: 
        await message.answer('Какое-то приветственное сообщение', reply_markup=ReplyKeyboardRemove())        
        # Вопрос №1 - Тип кредита
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Ипотека")],
                [KeyboardButton(text="Потребительский кредит")],
                [KeyboardButton(text="Авто-кредит")],
                [KeyboardButton(text="Микрозайм")],
                [KeyboardButton(text="Кредит под залог")]
            ],
            resize_keyboard=True
        )
        await message.answer('Выберите тип кредита:\n\n(Нажмите кнопку в всплывающем меню)', reply_markup=kb)
        await state.set_state(model_main.Form.credit_type)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'start'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №1 - Тип кредита
@dp.message(F.text, model_main.Form.credit_type)
async def credit_type(message: Message, state: FSMContext):
    try:
        # В зависимости от типа кредита мы уходим в отдельные ветки под эти кредиты
        if message.text == 'Ипотека':
            pass
            # await state.update_data(credit_type=message.text)
            # await message.answer('Переходим в ветку ипотека')
            # await state.set_state(model_ipoteka.Form.ipoteka_test)
        elif message.text == 'Потребительский кредит':
            pass
        elif message.text == 'Авто-кредит':
            pass
        elif message.text == 'Микрозайм':

            # Вопрос №1 - Срок кредита
            keyboard=[]
            for year in range(1, 8):
                keyboard.append([KeyboardButton(text=f"{year}")])
            kb = ReplyKeyboardMarkup(
                keyboard=keyboard,
                resize_keyboard=True
            )
            await message.answer(f'Выберите срок кредита. Для вашего варианта максимальный срок - 7 лет:\n\n(Нажмите кнопку в всплывающем меню)', reply_markup=kb)
            await state.set_state(model_microloan.Form.M_credit_period)
        elif message.text == 'Кредит под залог':

            # Вопрос - Имеется ли у вас квартира или дом?
            await message.answer("Имеется ли у вас квартира или дом?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
            await state.set_state(model_credit_pod_zalog.Form.CPZ_apartment_or_house)
            


        # if message.text in ['Ипотека', 'Потребительский кредит', 'Авто-кредит', 'Микрозайм', 'Кредит под залог']:
        #     await state.update_data(credit_type=message.text)
        #     if message.text in ['Ипотека']:
        #         # Вопрос №1.1 - Вид кредита (Если тип кредита - "Ипотека")
        #         for mes in description_credit:
        #             await message.answer(mes)
        #         kb = ReplyKeyboardMarkup(
        #             keyboard=[
        #                 [KeyboardButton(text="Дальневосточная")],
        #                 [KeyboardButton(text="Сельская")],
        #                 [KeyboardButton(text="IT")],
        #                 [KeyboardButton(text="Арктическая")],
        #                 [KeyboardButton(text="Семейная")],
        #                 [KeyboardButton(text="Нельготная")]
        #             ],
        #             resize_keyboard=True
        #         )
        #         await message.answer('Выберите вид ипотеки:\n\n(Нажмите кнопку в всплывающем меню)', reply_markup=kb)
        #         await state.set_state(Form.ipoteka_type)
        #     elif message.text == 'Кредит под залог':
        #         await message.answer("Имеется ли у вас квартира или дом?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
        #         await state.set_state(Form.apartment_or_house)

        #     elif message.text in ['Потребительский кредит', 'Авто-кредит', 'Микрозайм', 'Кредит под залог']:
        #         await state.update_data(ipoteka_type='')

        #         # Вопрос №1.2 - Срок кредита
        #         kb = ReplyKeyboardMarkup(
        #             keyboard=[
        #                 [KeyboardButton(text="1 месяц")],
        #                 [KeyboardButton(text="2 месяца")],
        #                 [KeyboardButton(text="3 месяца")],
        #                 [KeyboardButton(text="4 месяца")],
        #                 [KeyboardButton(text="5 месяцев")],
        #                 [KeyboardButton(text="6 месяцев")],
        #                 [KeyboardButton(text="7 месяцев")],
        #                 [KeyboardButton(text="8 месяцев")],
        #                 [KeyboardButton(text="9 месяцев")],
        #                 [KeyboardButton(text="10 месяцев")],
        #                 [KeyboardButton(text="11 месяцев")],
        #                 [KeyboardButton(text="1 год")],
        #                 [KeyboardButton(text="2 года")],
        #                 [KeyboardButton(text="3 года")],
        #                 [KeyboardButton(text="4 года")],
        #                 [KeyboardButton(text="5 лет")],
        #                 [KeyboardButton(text="6 лет")],
        #                 [KeyboardButton(text="7 лет")]
        #             ],
        #             resize_keyboard=True
        #         )
        #         await message.answer(f'Выберите срок кредита. Максимальный срок - 7 лет:\n\n(Нажмите кнопку в всплывающем меню)', reply_markup=kb)
        #         await state.set_state(Form.credit_period)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'credit_type'")
        await message.answer("Произошла ошибка. Попробуйте позже.")





# # СТАРАЯ ВЕРСИЯ НИЖЕ

# # Обработка вопроса №1 - Тип кредита
# @dp.message(F.text, Form.credit_type)
# async def credit_type(message: Message, state: FSMContext):
#     try:
#         if message.text in ['Ипотека', 'Потребительский кредит', 'Авто-кредит', 'Микрозайм', 'Кредит под залог']:
#             await state.update_data(credit_type=message.text)
#             if message.text in ['Ипотека']:
#                 # Вопрос №1.1 - Вид кредита (Если тип кредита - "Ипотека")
#                 for mes in description_credit:
#                     await message.answer(mes)
#                 kb = ReplyKeyboardMarkup(
#                     keyboard=[
#                         [KeyboardButton(text="Дальневосточная")],
#                         [KeyboardButton(text="Сельская")],
#                         [KeyboardButton(text="IT")],
#                         [KeyboardButton(text="Арктическая")],
#                         [KeyboardButton(text="Семейная")],
#                         [KeyboardButton(text="Нельготная")]
#                     ],
#                     resize_keyboard=True
#                 )
#                 await message.answer('Выберите вид ипотеки:\n\n(Нажмите кнопку в всплывающем меню)', reply_markup=kb)
#                 await state.set_state(Form.ipoteka_type)
#             elif message.text == 'Кредит под залог':
#                 await message.answer("Имеется ли у вас квартира или дом?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
#                 await state.set_state(Form.apartment_or_house)

#             elif message.text in ['Потребительский кредит', 'Авто-кредит', 'Микрозайм', 'Кредит под залог']:
#                 await state.update_data(ipoteka_type='')

#                 # Вопрос №1.2 - Срок кредита
#                 kb = ReplyKeyboardMarkup(
#                     keyboard=[
#                         [KeyboardButton(text="1 месяц")],
#                         [KeyboardButton(text="2 месяца")],
#                         [KeyboardButton(text="3 месяца")],
#                         [KeyboardButton(text="4 месяца")],
#                         [KeyboardButton(text="5 месяцев")],
#                         [KeyboardButton(text="6 месяцев")],
#                         [KeyboardButton(text="7 месяцев")],
#                         [KeyboardButton(text="8 месяцев")],
#                         [KeyboardButton(text="9 месяцев")],
#                         [KeyboardButton(text="10 месяцев")],
#                         [KeyboardButton(text="11 месяцев")],
#                         [KeyboardButton(text="1 год")],
#                         [KeyboardButton(text="2 года")],
#                         [KeyboardButton(text="3 года")],
#                         [KeyboardButton(text="4 года")],
#                         [KeyboardButton(text="5 лет")],
#                         [KeyboardButton(text="6 лет")],
#                         [KeyboardButton(text="7 лет")]
#                     ],
#                     resize_keyboard=True
#                 )
#                 await message.answer(f'Выберите срок кредита. Максимальный срок - 7 лет:\n\n(Нажмите кнопку в всплывающем меню)', reply_markup=kb)
#                 await state.set_state(Form.credit_period)
#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'credit_type'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


# # Обработка вопроса №1.1 - Вид кредита (Если тип кредита - "Ипотека")
# @dp.message(F.text, Form.ipoteka_type)
# async def credit_type(message: Message, state: FSMContext):
#     try:
#         if message.text in ['Дальневосточная', 'Сельская', 'IT', 'Арктическая', 'Семейная', 'Нельготная']:
#             await state.update_data(ipoteka_type=message.text)

#             # Вопрос №1.2 - Срок кредита (Для ипотеки)
#             if message.text in ['Дальневосточная', 'IT', 'Арктическая', 'Семейная']: max_credit_time = 20
#             elif message.text == 'Сельская': max_credit_time = 25
#             elif message.text == 'Нельготная': max_credit_time = 30

#             keyboard=[]
#             for year in range(1, max_credit_time+1):
#                 keyboard.append([KeyboardButton(text=f"{year}")])
                
#             kb = ReplyKeyboardMarkup(
#                 keyboard=keyboard,
#                 resize_keyboard=True
#             )
#             await message.answer(f'Выберите срок кредита. Для вашего варианта максимальный срок - {max_credit_time} лет:\n\n(Нажмите кнопку в всплывающем меню)', reply_markup=kb)
#             await state.set_state(Form.credit_period)
#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'ipoteka_type'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


# # Обработка вопроса №1.2 - Срок кредита
# @dp.message(F.text, Form.credit_period)
# async def credit_period(message: Message, state: FSMContext):
#     try:
#         if message.text in allowable_credit_time:
#             await state.update_data(credit_period=message.text)

#             # Вопрос №1.3 - Сумма кредита
#             await message.answer('Введите сумму кредита:', reply_markup=ReplyKeyboardRemove())
#             await state.set_state(Form.credit_sum)
#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'credit_period'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


# # Обработка вопроса №1.3 - Сумма кредита
# @dp.message(F.text, Form.credit_sum)
# async def credit_sum(message: Message, state: FSMContext):
#     try:
#         sum = ''.join(re.findall(r'\d+', message.text))
#         await state.update_data(credit_sum=sum)

#         # Если тип кредита Ипотека, то спрашивает про первоначальный взнос
#         data = await state.get_data()
#         credit_type = data.get("credit_type")
#         if credit_type == 'Ипотека':
#             # Вопрос №1.4 - Размер первого депозита
#             await message.answer("Какой ваш первоначальный взнос? (Он должен быть не меньше 15% от суммы кредита)", reply_markup=ReplyKeyboardRemove())
#             await state.set_state(Form.first_payment)




#         # TODO
#         else:
#             await state.update_data(first_payment='')

#             # Вопрос №2 - Регион
#             await message.answer("Регион, где планируете взять ипотеку?", reply_markup=ReplyKeyboardRemove())
#             await state.set_state(Form.region)


#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'credit_sum'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


# # Обработка вопроса №1.4 - Размер первого депозита
# @dp.message(F.text, Form.first_payment)
# async def first_payment(message: Message, state: FSMContext):
#     try:
#         # Депозит
#         deposit = ''.join(re.findall(r'\d+', message.text))
#         # Сумма кредита
#         data = await state.get_data()
#         credit_sum = data.get("credit_sum")
#         # Процентное соотношение
#         percent = int(deposit)*100/int(credit_sum)
#         if percent < 15:
#             # Если первый депозит все-таки меньше 15%:
#             await message.answer("Эта сумма для первого депозита меньше 15%. Необходимо увеличить первоначальный взнос")
#             await message.answer("Какой ваш первоначальный взнос? (Он должен быть не меньше 15% от суммы кредита)")
#             await state.set_state(Form.first_payment)
#         else:
#             # Если первый депозит больше 15%:
#             await state.update_data(first_payment=deposit)

#             # Вопрос №2 - Регион
#             await message.answer("Регион, где планируете взять ипотеку?")
#             await state.set_state(Form.region)         
#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'first_payment'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


# # Обработка вопроса №2 - Регион
# @dp.message(F.text, Form.region)
# async def region(message: Message, state: FSMContext):
#     try:
#         await state.update_data(region=message.text)

#         # Вопрос №3 - Являетесь ли вы резидентом РФ?
#         await message.answer("Являетесь ли вы резидентом РФ?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
#         await state.set_state(Form.is_rezident)
#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'region")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


# # Обработка вопроса №3 - Являетесь ли вы резидентом РФ?
# @dp.message(F.text, Form.is_rezident)
# async def is_rezident(message: Message, state: FSMContext):
#     try:
#         if message.text in ["Да", "Нет"]:
#             await state.update_data(is_rezident=message.text)
#             if message.text == "Да":
#                 await state.update_data(registration='')
#                 # Вопрос №4 - Есть ли судимость?
#                 await message.answer("Есть ли у вас судимость?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
#                 await state.set_state(Form.is_сriminal_record)    
#             if message.text == "Нет":
#                 # Вопрос №3.1 - Есть ли регистрация на территории РФ и вид на жительство?
#                 await message.answer("У вас есть регистрация на территории РФ и вид на жительство?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
#                 await state.set_state(Form.registration)
#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'is_rezident'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


# # Обработка вопроса №3.1 -  Есть ли регистрация на территории РФ и вид на жительство?
# @dp.message(F.text, Form.registration)
# async def registration(message: Message, state: FSMContext):
#     try:
#         if message.text in ["Да", "Нет"]:
#             await state.update_data(registration=message.text)

#             # Вопрос №4 - Есть ли судимость?
#             await message.answer("Есть ли у вас судимость?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
#             await state.set_state(Form.is_сriminal_record)
#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'registration'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


# # Обработка вопроса №4 - Есть ли судимость?
# @dp.message(F.text, Form.is_сriminal_record)
# async def is_сriminal_record(message: Message, state: FSMContext):
#     try:
#         if message.text in ["Да", "Нет"]:
#             await state.update_data(is_сriminal_record=message.text)
#             if message.text == "Да":
#                 # Вопрос №4.1 - По экономической статье?
#                 await message.answer("По экономической статье?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
#                 await state.set_state(Form.сriminal_record_econom)
#             if message.text == "Нет":
#                 await state.update_data(сriminal_record_econom='')

#                 # Вопрос №5 - Есть ли исполнительные производства в ФССП (Федеральная служба судебных приставов)?
#                 await message.answer("Есть ли у вас исполнительные производства в ФССП (Федеральная служба судебных приставов)?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
#                 await state.set_state(Form.fssp)
#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'is_сriminal_record'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


# # Обработка вопроса №4.1 - По экономической статье?
# @dp.message(F.text, Form.сriminal_record_econom)
# async def сriminal_record_econom(message: Message, state: FSMContext):
#     try:
#         if message.text in ["Да", "Нет"]:
#             await state.update_data(сriminal_record_econom=message.text)

#             # Вопрос №5 - Есть ли исполнительные производства в ФССП (Федеральная служба судебных приставов)?
#             await message.answer("Есть ли у вас исполнительные производства в ФССП (Федеральная служба судебных приставов)?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
#             await state.set_state(Form.fssp)
#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'сriminal_record_econom'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


# # Обработка вопроса №5 - Есть ли у Вас исполнительные производства в ФССП (Федеральная служба судебных приставов)?
# @dp.message(F.text, Form.fssp)
# async def fssp(message: Message, state: FSMContext):
#     try:
#         if message.text in ["Да", "Нет"]:
#             await state.update_data(fssp=message.text)

#             # Вопрос №6 - Являетесь ли вы зарплатником банка?
#             await message.answer("Являетесь ли Вы зарплатником банка?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
#             await state.set_state(Form.bank_salary)
#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'fssp'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


# # Обработка вопроса №6 - Являетесь ли вы зарплатником банка?
# @dp.message(F.text, Form.bank_salary)
# async def bank_salary(message: Message, state: FSMContext):
#     try:
#         if message.text in ["Да", "Нет"]:
#             await state.update_data(bank_salary=message.text)
#             if message.text == "Да":
#                 # Вопрос №6.1 - Какого банка?
#                 await message.answer("Зарплатником какого банка вы являетесь?", reply_markup=ReplyKeyboardRemove())
#                 await state.set_state(Form.bank_name)
#             if message.text == "Нет":
#                 await state.update_data(bank_name=message.text)

#                 # Вопрос №7 - Кредитный рейтинг?
#                 kb = ReplyKeyboardMarkup(
#                     keyboard=[
#                         [KeyboardButton(text="Загрузить PDF с кредитной историей")],
#                         [KeyboardButton(text="Ввести кредитный рейтинг самостоятельно")],
#                         [KeyboardButton(text="Пропустить")]
#                     ],
#                     resize_keyboard=True
#                 )
#                 await message.answer("Каким образом вам будет удобнее поделиться кредитным рейтингом?\n\n - Загрузить PDF с кредитной историей\n(Самый точный результат)\n - Ввести кредитный рейтинг самостоятельно\n(Менее точный результат)\n - Пропустить\n(Приблизительный результат)", reply_markup=kb)
#                 await state.set_state(Form.credit_rating)

#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'bank_salary'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


# # Обработка вопроса №6.1 - Какого банка?
# @dp.message(F.text, Form.bank_name)
# async def bank_name(message: Message, state: FSMContext):
#     try:
#         await state.update_data(bank_name=message.text)
        
#         # Вопрос №7 - Кредитный рейтинг?
#         kb = ReplyKeyboardMarkup(
#             keyboard=[
#                 [KeyboardButton(text="Загрузить PDF с кредитной историей")],
#                 [KeyboardButton(text="Ввести кредитный рейтинг самостоятельно")],
#                 [KeyboardButton(text="Пропустить")]
#             ],
#             resize_keyboard=True
#         )
#         await message.answer("Каким образом вам будет удобнее поделиться кредитным рейтингом?\n\n - Загрузить PDF с кредитной историей\n(Самый точный результат)\n - Ввести кредитный рейтинг самостоятельно\n(Менее точный результат)\n - Пропустить\n(Приблизительный результат)", reply_markup=kb)
#         await state.set_state(Form.credit_rating)
#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'bank_name'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №7 - Кредитный рейтинг?
# @dp.message(F.text, Form.credit_rating)
# async def credit_rating(message: Message, state: FSMContext):
#     try:
#         if message.text in ["Да", "Нет"]:

#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'credit_rating'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")



# @dp.message(F.text, Form.fssp)
# async def fssp(message: Message, state: FSMContext):
#     try:
#         if message.text in ["Да", "Нет"]:

#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'fssp'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


# @dp.message(F.text, Form.fssp)
# async def fssp(message: Message, state: FSMContext):
#     try:
#         if message.text in ["Да", "Нет"]:

#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'fssp'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


# @dp.message(F.text, Form.fssp)
# async def fssp(message: Message, state: FSMContext):
#     try:
#         if message.text in ["Да", "Нет"]:

#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'fssp'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


# @dp.message(F.text, Form.finish)  
# async def finish(message: Message, state: FSMContext):
#     try:
#         if message.text == "✅Отправил": 
#             await message.answer_photo(photo=FSInputFile('media/last_message_photo.jpg'), caption="Спасибо, что воспользовались нашим ботом!\nВ ближайшее время *наш менеджер Вам позвонит*.\nУспехов в одобрении!\n\nИнформацию по другим услугам можете узнать на нашем сайте или в профиле компании в яндексе:\n\n*Сайт*:\nhttps://ystroim-vseh.clients.site/\n\n*Наша компания в яндексе*:\nhttps://yandex.ru/profile/13064319362\n\n*Дополнительный сайт*:\nhttps://ystroim-vsekh.ru/", reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")
            
#             data = await state.get_data()
#             response = await post_exel(message.from_user.id, data)
#             await state.clear()
#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'finish'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")


if __name__ == '__main__':
    asyncio.run(main())

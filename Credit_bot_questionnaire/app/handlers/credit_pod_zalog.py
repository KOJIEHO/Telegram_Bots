from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from datetime import datetime
import logging
import re

from app.model.model_credit_pod_zalog import Form
from app.model import model_car_loan
from app.keyboards.keyboards import kb_yn

logging.basicConfig(
    filename="error_log.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.ERROR,
    encoding="utf-8"
)
logger = logging.getLogger(__name__)

allowable_credit_time = []
for x in range(1, 16):
    allowable_credit_time.append(f'{x}')


credit_pod_zalog_router = Router()


# TODO
# 1. доделать финансовую нагрузку
# 2. доделать итого (разобраться че там надо выводить и как считать)


# Обработка вопроса - Имеется ли у вас квартира или дом? 
@credit_pod_zalog_router.message(F.text, Form.CPZ_apartment_or_house)
async def CPZ_apartment_or_house(message: Message, state: FSMContext):
    try:
        await state.update_data(CPZ_credit_type='Кредит под залог')
        if message.text == "Да":
            await state.update_data(CPZ_apartment_or_house=message.text)

            # Вопрос - Срок кредита
            keyboard=[]
            for year in range(1, 16):
                keyboard.append([KeyboardButton(text=f"{year}")])
            kb = ReplyKeyboardMarkup(
                keyboard=keyboard,
                resize_keyboard=True
            )
            await message.answer(f'Выберите срок кредита. Для вашего варианта максимальный срок - 15 лет:\n\n(Нажмите кнопку в всплывающем меню)', reply_markup=kb)
            await state.set_state(Form.CPZ_credit_period)
        if message.text == "Нет":
            await state.update_data(CPZ_apartment_or_house=message.text)

            # Конец анкеты
            await message.answer("Ваш кредит не одобрят.\n\nИтог:\n - Отсутствует имущество под залог\n\nРекомендации:\n - Для кредита необходимо иметь имущество в виде квартиры или дома", reply_markup=ReplyKeyboardRemove())
            await state.clear()
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_apartment_or_house'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса - Срок кредита
@credit_pod_zalog_router.message(F.text, Form.CPZ_credit_period)
async def CPZ_credit_period(message: Message, state: FSMContext):
    try:
        if message.text in allowable_credit_time:
            await state.update_data(CPZ_credit_period=message.text)

            # Вопрос - Сумма кредита
            await message.answer('Введите сумму кредита:', reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.CPZ_credit_sum)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_credit_period'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса - Сумма кредита
@credit_pod_zalog_router.message(F.text, Form.CPZ_credit_sum)
async def CPZ_credit_sum(message: Message, state: FSMContext):
    try:
        sum = ''.join(re.findall(r'\d+', message.text))
        await state.update_data(CPZ_credit_sum=sum)

        # Вопрос - Размер первого депозита
        await message.answer("Первоначальный взнос кредита дложен составлять 50% от оценочной стоимости дома или квартиры")
        await message.answer("Имеется ли у вас имущество, подходящее под этот критерий?", reply_markup=kb_yn)
        await state.set_state(Form.CPZ_first_payment)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_credit_sum'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса - Размер первого депозита
@credit_pod_zalog_router.message(F.text, Form.CPZ_first_payment)
async def CPZ_first_payment(message: Message, state: FSMContext):
    try:
        if message.text == "Нет":
            await state.update_data(CPZ_first_payment=message.text)

            # Вопрос - Уменьшить сумму или уходим в автокредит
            kb = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Уменьшить сумму кредита")],
                    [KeyboardButton(text="Кредит под залог автомобиля")]
                ],
                resize_keyboard=True
            )
            await message.answer("В таком случае можем предложить два варианта:\n1. Уменьшить сумму кредита\n2. Проверить возможность взять кредит под залог автомобиля\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb)
            await state.set_state(Form.CPZ_reduce_credit_sum_or_autoloan)
        if message.text == "Да":
            await state.update_data(CPZ_first_payment=message.text)

            # Вопрос №2 - Регион
            await message.answer("Регион, где планируете взять ипотеку?")
            await state.set_state(Form.CPZ_region)         
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_first_payment'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса - Уменьшить сумму или уходим в автокредит
@credit_pod_zalog_router.message(F.text, Form.CPZ_reduce_credit_sum_or_autoloan)
async def CPZ_reduce_credit_sum_or_autoloan(message: Message, state: FSMContext):
    try:
        if message.text == "Уменьшить сумму кредита":
            # Перенавпряем обратно на Вопрос №3 - Сумма кредита
            await message.answer('Введите сумму кредита:', reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.CPZ_credit_sum)
        if message.text == "Кредит под залог автомобиля":
            # Перенаправляем в ветку Авто-кредит
            await message.answer('Необходимо проверить возможность взятия кредита под залог автомобиля', reply_markup=ReplyKeyboardRemove())
            await message.answer("Являетесь ли вы резидентом РФ?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
            await state.set_state(model_car_loan.Form.CL_is_rezident)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_reduce_credit_sum_or_autoloan'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №2 - Регион
@credit_pod_zalog_router.message(F.text, Form.CPZ_region)
async def CPZ_region(message: Message, state: FSMContext):
    try:
        await state.update_data(CPZ_region=message.text)

        # Вопрос №3 - Являетесь ли вы резидентом РФ?
        await message.answer("Являетесь ли вы резидентом РФ?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
        await state.set_state(Form.CPZ_is_rezident)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_region")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №3 - Являетесь ли вы резидентом РФ?
@credit_pod_zalog_router.message(F.text, Form.CPZ_is_rezident)
async def CPZ_is_rezident(message: Message, state: FSMContext):
    try:
        if message.text in ["Да", "Нет"]:
            await state.update_data(CPZ_is_rezident=message.text)
            if message.text == "Да":

                # Вопрос №4 - Есть ли судимость?
                await message.answer("Есть ли у вас судимость?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
                await state.set_state(Form.CPZ_is_сriminal_record)    
            if message.text == "Нет":

                # Вопрос №3.1 - Есть ли регистрация на территории РФ и вид на жительство?
                await message.answer("У вас есть регистрация на территории РФ и вид на жительство?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
                await state.set_state(Form.CPZ_registration)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_is_rezident'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №3.1 -  Есть ли регистрация на территории РФ и вид на жительство?
@credit_pod_zalog_router.message(F.text, Form.CPZ_registration)
async def CPZ_registration(message: Message, state: FSMContext):
    try:
        if message.text in ["Да", "Нет"]:
            await state.update_data(CPZ_registration=message.text)

            # Вопрос №4 - Есть ли судимость?
            await message.answer("Есть ли у вас судимость?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
            await state.set_state(Form.CPZ_is_сriminal_record)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_registration'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №4 - Есть ли судимость?
@credit_pod_zalog_router.message(F.text, Form.CPZ_is_сriminal_record)
async def CPZ_is_сriminal_record(message: Message, state: FSMContext):
    try:
        if message.text in ["Да", "Нет"]:
            await state.update_data(CPZ_is_сriminal_record=message.text)
            if message.text == "Да":
                # Вопрос №4.1 - По экономической статье?
                await message.answer("По экономической статье?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
                await state.set_state(Form.CPZ_сriminal_record_econom)
            if message.text == "Нет":
                await state.update_data(CPZ_сriminal_record_econom='')

                # Вопрос №5 - Есть ли исполнительные производства в ФССП (Федеральная служба судебных приставов)?
                await message.answer("Есть ли у вас исполнительные производства в ФССП (Федеральная служба судебных приставов)?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
                await state.set_state(Form.CPZ_fssp)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_is_сriminal_record'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №4.1 - По экономической статье?
@credit_pod_zalog_router.message(F.text, Form.CPZ_сriminal_record_econom)
async def CPZ_сriminal_record_econom(message: Message, state: FSMContext):
    try:
        if message.text in ["Да", "Нет"]:
            await state.update_data(CPZ_сriminal_record_econom=message.text)

            # Вопрос №5 - Есть ли исполнительные производства в ФССП (Федеральная служба судебных приставов)?
            await message.answer("Есть ли у вас исполнительные производства в ФССП (Федеральная служба судебных приставов)?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
            await state.set_state(Form.CPZ_fssp)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_сriminal_record_econom'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №5 - Есть ли у Вас исполнительные производства в ФССП (Федеральная служба судебных приставов)?
@credit_pod_zalog_router.message(F.text, Form.CPZ_fssp)
async def CPZ_fssp(message: Message, state: FSMContext):
    try:
        if message.text in ["Да", "Нет"]:
            await state.update_data(CPZ_fssp=message.text)

            # Вопрос №6 - Являетесь ли вы зарплатником банка?
            await message.answer("Являетесь ли Вы зарплатником банка?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
            await state.set_state(Form.CPZ_bank_salary)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_fssp'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №6 - Являетесь ли вы зарплатником банка?
@credit_pod_zalog_router.message(F.text, Form.CPZ_bank_salary)
async def CPZ_bank_salary(message: Message, state: FSMContext):
    try:
        if message.text in ["Да", "Нет"]:
            await state.update_data(CPZ_bank_salary=message.text)
            if message.text == "Да":

                # Вопрос №6.1 - Какого банка?
                await message.answer("Зарплатником какого банка вы являетесь?", reply_markup=ReplyKeyboardRemove())
                await state.set_state(Form.CPZ_bank_name)
            if message.text == "Нет":
                await state.update_data(CPZ_bank_name='')

                # Вопрос №7 - Кредитный рейтинг?
                kb = ReplyKeyboardMarkup(
                    keyboard=[
                        [KeyboardButton(text="Загрузить PDF с кредитной историей")],
                        [KeyboardButton(text="Ввести кредитный рейтинг самостоятельно")],
                        [KeyboardButton(text="Пропустить")]
                    ],
                    resize_keyboard=True
                )
                await message.answer("Каким образом вам будет удобнее поделиться кредитным рейтингом?\n\n - Загрузить PDF с кредитной историей\n(Самый точный результат)\n - Ввести кредитный рейтинг самостоятельно\n(Менее точный результат)\n - Пропустить\n(Приблизительный результат)", reply_markup=kb)
                await state.set_state(Form.CPZ_credit_rating)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_bank_salary'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №6.1 - Какого банка?
@credit_pod_zalog_router.message(F.text, Form.CPZ_bank_name)
async def CPZ_bank_name(message: Message, state: FSMContext):
    try:
        await state.update_data(CPZ_bank_name=message.text)
        
        # Вопрос №7 - Кредитный рейтинг?
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Загрузить PDF с кредитной историей")],
                [KeyboardButton(text="Ввести кредитный рейтинг самостоятельно")],
                [KeyboardButton(text="Пропустить")]
            ],
            resize_keyboard=True
        )
        await message.answer("Каким образом вам будет удобнее поделиться кредитным рейтингом?\n\n - Загрузить PDF с кредитной историей\n(Самый точный результат)\n - Ввести кредитный рейтинг самостоятельно\n(Менее точный результат)\n - Пропустить\n(Приблизительный результат)", reply_markup=kb)
        await state.set_state(Form.CPZ_credit_rating)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_bank_name'")
        await message.answer("Произошла ошибка. Попробуйте позже.")







# ТУТ НАДО ПОЧИНИТЬ ВСЮ ЭТУ ХЕРНЮ
# ---------------------------------------------------------------------------------
# Обработка вопроса №7 - Кредитный рейтинг?
@credit_pod_zalog_router.message(F.text, Form.CPZ_credit_rating)
async def CPZ_credit_rating(message: Message, state: FSMContext):
    try:
        if message.text == "Загрузить PDF с кредитной историей":

            # Вопрос №7.1 - Вынимаем кредитный рейтинг из PDF файла
            await message.answer("Отправьте PDF файл с кредитной историей", reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.CPZ_credit_rating_PDF)
        elif message.text == "Ввести кредитный рейтинг самостоятельно":
            pass
            # Вопрос №7.2 - Какой ваш кредитный рейтинг? 
            # await message.answer("Введите свой кредитный рейтинг", reply_markup=ReplyKeyboardRemove())
            # await state.set_state(Form.CPZ_credit_rating_PDF)
        elif message.text == "Пропустить":
            pass
            # 

    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_credit_rating'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №7.1 - Вынимаем кредитный рейтинг из PDF файла
@credit_pod_zalog_router.message(F.text, Form.CPZ_credit_rating_PDF)
async def CPZ_credit_rating_PDF(message: Message, state: FSMContext):
    try:

            # TODO
            # Обработку изображения
            credit_rating = 'tmp'


            await state.update_data(CPZ_credit_rating=credit_rating)

            # Вопрос №10.3 - Что брали из действующих кредитов?
            await message.answer("Что брали из действующих кредитов?", reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.CPZ_FB_credit)

    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_credit_rating_PDF'")
        await message.answer("Произошла ошибка. Попробуйте позже.")



# Тут надо будет добавлять промежуточное состояние, чтобы обработать pdf файл


# Обработка вопроса №10.3 - Что брали из действующих кредитов?
@credit_pod_zalog_router.message(F.text, Form.CPZ_FB_credit)
async def CPZ_FB_credit(message: Message, state: FSMContext):
    try:


        # TODO
        # Обработку изображения
        credit_rating = 'tmp'


        await state.update_data(CPZ_credit_rating=credit_rating)

        # Вопрос №10.3 - Что брали из действующих кредитов?
        await message.answer("Что брали из действующих кредитов?", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.CPZ_FB_credit)

    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_FB_credit'")
        await message.answer("Произошла ошибка. Попробуйте позже.")
# ---------------------------------------------------------------------






# Обработка вопроса №9 - Есть ли действующая просрочка?
@credit_pod_zalog_router.message(F.text, Form.CPZ_delay)
async def CPZ_delay(message: Message, state: FSMContext):
    try:
        if message.text in ["Да", "Нет"]:
            await state.update_data(CPZ_delay=message.text)

            # Вопрос №10 - Введите дату своего рождения
            await message.answer("Введите дату своего рождения в формате:\nдд.мм.гггг", reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.CPZ_birthday)

    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_delay'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №10 - Введите дату своего рождения
@credit_pod_zalog_router.message(F.text, Form.CPZ_birthday)
async def CPZ_birthday(message: Message, state: FSMContext):
    try:
        try:
            birth_date = datetime.strptime(message.text, "%d.%m.%Y").date()
        except ValueError:
            await message.answer("Неверный формат. Используйте ДД.ММ.ГГГГ") 
        await state.update_data(CPZ_birthday=message.text)

        # Вопрос №11 - Ваше семейное положение
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Состою В браке")],
                [KeyboardButton(text="Не состою в браке")]
            ],
            resize_keyboard=True
        )
        await message.answer("Ваше семейное положение\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb)
        await state.set_state(Form.CPZ_family_status)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_birthday'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №11 - Ваше семейное положение
@credit_pod_zalog_router.message(F.text, Form.CPZ_family_status)
async def CPZ_family_status(message: Message, state: FSMContext):
    try:
        if message.text in ["Состою В браке", "Не состою в браке"]:
            await state.update_data(CPZ_family_status=message.text)

            # Вопрос №12 - Количество детей
            await message.answer("Укажите количество детей, которое указано в паспорте", reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.CPZ_number_of_children)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_family_status'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №12 - Количество детей
@credit_pod_zalog_router.message(F.text, Form.CPZ_number_of_children)
async def CPZ_number_of_children(message: Message, state: FSMContext):
    try:
        number_of_children = int(''.join(re.findall(r'\d+', message.text)))
        if number_of_children < 0:
            await message.answer("Число должно быть положительным. Попробуйте снова.")
            return
        await state.update_data(CPZ_number_of_children = number_of_children)
        await state.update_data(CPZ_childrens_birthdays = [])
        await state.update_data(CPZ_current_child_index = 0)

        if number_of_children > 0:
            
            # Вопрос №13 - Даты рождения детей
            data = await state.get_data()
            current_index = data['CPZ_current_child_index']
            await message.answer(f"Введите дату рождения ребенка №{current_index + 1} (дд.мм.гггг):", reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.CPZ_childrens_birthdays)
        else:

            # Вопрос №14 - Количество иждивенцев 
            await message.answer("Укажите количество иждивенцев (Не считая детей по паспорту)", reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.CPZ_is_izdiventsi)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_number_of_children'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


async def ask_child_birthday(message: Message, state: FSMContext, child_num: int):
    """Функция запроса даты рождения конкретного ребенка"""

    await message.answer(f"Введите дату рождения ребенка №{child_num} (ДД.ММ.ГГГГ):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.CPZ_childrens_birthdays)


@credit_pod_zalog_router.message(F.text, Form.CPZ_childrens_birthdays)
async def CPZ_childrens_birthdays(message: Message, state: FSMContext):
    try:
        try:
            birth_date = datetime.strptime(message.text, "%d.%m.%Y").date()
        except ValueError:
            await message.answer("Неверный формат. Используйте ДД.ММ.ГГГГ")

        today = datetime.now().date()
        
        if birth_date > today:
            await message.answer("Дата рождения не может быть в будущем. Попробуйте снова.")
            return
            
        data = await state.get_data()
        childrens_birthdays = data['CPZ_childrens_birthdays']
        childrens_birthdays.append(message.text)
        current_index = data['CPZ_current_child_index'] + 1
        
        await state.update_data(CPZ_childrens_birthdays = childrens_birthdays)
        await state.update_data(CPZ_current_child_index = current_index)
        
        # Проверяем, остались ли еще дети
        if current_index < data['CPZ_number_of_children']:
            await ask_child_birthday(message, state, current_index + 1)
        else:
            await message.answer("Укажите количество иждивенцев (Не считая детей по паспорту)", reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.CPZ_is_izdiventsi)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_childrens_birthdays'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №14 - Количество иждивенцев
@credit_pod_zalog_router.message(F.text, Form.CPZ_is_izdiventsi)
async def CPZ_is_izdiventsi(message: Message, state: FSMContext):
    try:
        number_of_izdiventsi = ''.join(re.findall(r'\d+', message.text))
        await state.update_data(CPZ_is_izdiventsi=number_of_izdiventsi)

        # Вопрос - Подтверждение дохода
        await message.answer("Есть ли подтверждение вашего дохода?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
        await state.set_state(Form.CPZ_salary_proof)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_is_izdiventsi'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса - Подтверждение дохода
@credit_pod_zalog_router.message(F.text, Form.CPZ_salary_proof)
async def CPZ_salary_proof(message: Message, state: FSMContext):
    try:
        if message.text in ["Да", "Нет"]:    
            await state.update_data(CPZ_salary_proof=message.text)

            # Вопрос №15 - Тип заработной платы
            kb = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Официальная")],
                    [KeyboardButton(text="Неофициальная")],
                    [KeyboardButton(text="Комбинированная")]
                    ],
                resize_keyboard=True
            )
            await message.answer("Укажите тип вашей заработной платы\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb)
            await state.set_state(Form.CPZ_salary_type)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_salary_proof'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №15 - Тип зароботной плата
@credit_pod_zalog_router.message(F.text, Form.CPZ_salary_type)
async def CPZ_salary_type(message: Message, state: FSMContext):
    try:
        if message.text in ["Официальная", "Неофициальная", "Комбинированная"]:
            await state.update_data(CPZ_salary_type=message.text)

            # Вопрос №15.1 - Сумма заработной платы
            await message.answer("Напишите размер вашей заработной платы (в рублях)", reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.CPZ_salary_size)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_salary_type'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №15.1 - Сумма заработной платы
@credit_pod_zalog_router.message(F.text, Form.CPZ_salary_size)
async def CPZ_salary_size(message: Message, state: FSMContext):
    try:
        sum = ''.join(re.findall(r'\d+', message.text))
        await state.update_data(CPZ_salary_size=sum)

        # Вопрос №16 - Стаж работы
        await message.answer("Укажите стаж работы на последнем месте. С какой даты?\nВ формате:\nдд.мм.гггг", reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.CPZ_work_experience)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_salary_size'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №16 - Стаж работы
@credit_pod_zalog_router.message(F.text, Form.CPZ_work_experience)
async def CPZ_work_experience(message: Message, state: FSMContext):
    try:
        await state.update_data(CPZ_work_experience=message.text)

        # Вопрос №18 - Образование
        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Высшее")],
                [KeyboardButton(text="Среднее специальное")],
                [KeyboardButton(text="Среднее техническое")],
                [KeyboardButton(text="Среднее общее")],
                [KeyboardButton(text="Основное общее")]
                ],
            resize_keyboard=True
        )
        await message.answer("Укажите ваше образование\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb)
        await state.set_state(Form.CPZ_education)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_work_experience'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №18 - Образование
@credit_pod_zalog_router.message(F.text, Form.CPZ_education)
async def CPZ_education(message: Message, state: FSMContext):
    try:
        if message.text in ["Высшее", "Среднее специальное", "Среднее техническое", "Среднее общее", "Основное общее"]:
            await state.update_data(CPZ_education=message.text)

            # Вопрос №20 - Являетесь ли вы созаемщиком/поручителем другого кредита?
            await message.answer("Являетесь ли вы созаемщиком/поручителем другого кредита?\n\n(Нажмите кнопку в всплывающем меню)", reply_markup=kb_yn)
            await state.set_state(Form.CPZ_borrower)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_education'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №20 - Являетесь ли вы созаемщиком/поручителем другого кредита?
# Окончание анкеты, вывод по ответам
@credit_pod_zalog_router.message(F.text, Form.CPZ_borrower)
async def CPZ_borrower(message: Message, state: FSMContext):
    try:
        if message.text in ["Да", "Нет"]:
            await state.update_data(CPZ_borrower=message.text)

            # Подводим итоги
            message_result = 'Итог:\n '
            message_recommendations = 'Рекомендации:\n - Имущество оценивается со стороны банка, отсюда и формулировка "50% от оценочной стоимости"\n '
         
            data = await state.get_data()
            if data.get("CPZ_fssp") == 'Да':
                message_result += '- Будет отказ\n - Необходимо убрать исполнительное производство'
                message_recommendations += '- Проверить, что исполнительное производство убрали с сайта ФССП'
            
            if data.get("CPZ_salary_type") in ["Официальная", "Комбинированная", "Неофициальная"]:
                if (data.get("CPZ_salary_type") in ["Официальная", "Комбинированная"]) and (data.get("CPZ_bank_salary") == 'Да'):
                    message_recommendations += '- Обратитесь в ваш банк. Банк доверяет своим клиентам, поэтому больше шанс получить одобрение кредита\n '
                if data.get("CPZ_salary_type") == "Неофициальная":
                    message_recommendations += '- Требуется справка по форме банка\n '
                
                # Логика на вопросе №8
                




            # TODO
            # ОБРАБОТКА ВСЕХ ОТВЕТОВ
            

            # Конец анкеты
            await message.answer(message_result, reply_markup=ReplyKeyboardRemove())
            await message.answer(message_recommendations, reply_markup=ReplyKeyboardRemove())
            await state.clear()



    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_borrower'")
        await message.answer("Произошла ошибка. Попробуйте позже.")
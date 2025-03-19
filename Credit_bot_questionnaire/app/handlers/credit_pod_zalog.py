from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
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


@credit_pod_zalog_router.message(F.text, Form.CPZ_apartment_or_house)
async def CPZ_apartment_or_house(message: Message, state: FSMContext):
    try:
        await state.update_data(CPZ_credit_type='Кредит под залог')
        if message.text == "Да":
            await state.update_data(CPZ_apartment_or_house=message.text)

            # Вопрос №2 - Срок кредита
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


# Обработка вопроса №2 - Срок кредита
@credit_pod_zalog_router.message(F.text, Form.CPZ_credit_period)
async def CPZ_credit_period(message: Message, state: FSMContext):
    try:
        if message.text in allowable_credit_time:
            await state.update_data(CPZ_credit_period=message.text)

            # Вопрос №3 - Сумма кредита
            await message.answer('Введите сумму кредита:', reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.CPZ_credit_sum)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_credit_period'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №3 - Сумма кредита
@credit_pod_zalog_router.message(F.text, Form.CPZ_credit_sum)
async def CPZ_credit_sum(message: Message, state: FSMContext):
    try:
        sum = ''.join(re.findall(r'\d+', message.text))
        await state.update_data(CPZ_credit_sum=sum)

        # Вопрос №4 - Размер первого депозита
        await message.answer("Первоначальный взнос кредита дложен составлять 50% от оценочной стоимости дома или квартиры")
        await message.answer("Имеется ли у вас имущество, подходящее под этот критерий?", reply_markup=kb_yn)
        await state.set_state(Form.CPZ_first_payment)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_credit_sum'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №4 - Размер первого депозита
@credit_pod_zalog_router.message(F.text, Form.CPZ_first_payment)
async def CPZ_first_payment(message: Message, state: FSMContext):
    try:
        if message.text == "Нет":
            await state.update_data(CPZ_first_payment=message.text)

            # Вопрос №4.1 - Уменьшить сумму или уходим в автокредит
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
            pass


            # TODO Обработка фин нагрузки и прочего




    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_first_payment'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №4.1 - Уменьшить сумму или уходим в автокредит
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
            print('Прлбунем Мы в ветке Авто-кредит')
            await state.set_state(model_car_loan.Form.CL_is_rezident)
            print('Прлбунем Мы выРОЫВаоваовао ветке Авто-кредит')


            # TODO Перевод на Автокредит




    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CPZ_reduce_credit_sum_or_autoloan'")
        await message.answer("Произошла ошибка. Попробуйте позже.")

from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
import logging
import re

from app.model.model_ipoteka import Form
from app.keyboards.keyboards import kb_yn

logging.basicConfig(
    filename="error_log.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.ERROR,
    encoding="utf-8"
)
logger = logging.getLogger(__name__)


ipoteka_router = Router()


@ipoteka_router.message(F.text, Form.ipoteka_test)
async def apartment_or_house(message: Message, state: FSMContext):
    try:
        await message.answer(f'Перешли в ветку тест')
        await state.update_data(ipoteka_test=message.text)

        data = await state.get_data()
        await message.answer(f'{data.get("credit_type")}\n{data.get("ipoteka_test")}')




        # if message.text == "Да":
        #     # Вопрос №2 - Срок кредита
        #     await state.update_data(credit_pod_zalog_router=message.text)

        #     keyboard=[]
        #     for year in range(1, 16):
        #         keyboard.append([KeyboardButton(text=f"{year}")])
        #     kb = ReplyKeyboardMarkup(
        #         keyboard=keyboard,
        #         resize_keyboard=True
        #     )
        #     await message.answer(f'Выберите срок кредита. Для вашего варианта максимальный срок - 15 лет:\n\n(Нажмите кнопку в всплывающем меню)', reply_markup=kb)
        #     await state.set_state(Form.credit_period)
        # if message.text == "Нет":
        #     await state.update_data(credit_pod_zalog_router=message.text)

        #     # Конец анкеты
        #     await message.answer("Ваш кредит не одобрят.\n\nИтог:\n - Отсутствует имущество под залог\n\nРекомендации:\n - Для кредита необходимо иметь имущество в виде квартиры или дома", reply_markup=ReplyKeyboardRemove())
        #     await state.clear()
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'credit_pod_zalog_router'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# # Обработка вопроса №2 - Срок кредита
# @ipoteka_router.message(F.text, Form.credit_period)
# async def credit_period(message: Message, state: FSMContext):
#     try:
#         if message.text in allowable_credit_time:
#             await state.update_data(credit_period=message.text)
#             # Вопрос №3 - Сумма кредита
#             await message.answer('Введите сумму кредита:', reply_markup=ReplyKeyboardRemove())
#             await state.set_state(Form.credit_sum)
#     except Exception as exception:
#         logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'credit_period'")
#         await message.answer("Произошла ошибка. Попробуйте позже.")

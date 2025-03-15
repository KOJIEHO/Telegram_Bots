from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
import logging
import re

from app.model.model_car_loan import Form
from app.keyboards.keyboards import kb_yn

logging.basicConfig(
    filename="error_log.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.ERROR,
    encoding="utf-8"
)
logger = logging.getLogger(__name__)


car_loan_router = Router()


@car_loan_router.message(F.text, Form.CL_is_rezident)
async def CL_is_rezident(message: Message, state: FSMContext):
    try:
        await state.update_data(CPZ_credit_type='Кредит под залог')
        print('Мы в ветке Авто-кредит')
        await message.answer('Мы в ветке Авто-кредит')
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'CL_is_rezident'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# # Обработка вопроса №2 - Срок кредита
# @car_loan_router .message(F.text, Form.credit_period)
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

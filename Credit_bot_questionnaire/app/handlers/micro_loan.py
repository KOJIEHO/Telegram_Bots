from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
import logging
import re

from app.model.model_microloan import Form
from app.keyboards.keyboards import kb_yn

logging.basicConfig(
    filename="error_log.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.ERROR,
    encoding="utf-8"
)
logger = logging.getLogger(__name__)


micro_loan_router = Router()


# Обработка вопроса №1 - Срок кредита
@micro_loan_router.message(F.text, Form.M_credit_period)
async def M_credit_period(message: Message, state: FSMContext):
    try:
        if message.text in ["1", "2", "3", "4", "5", "6", "7"]:
            await state.update_data(M_credit_period=message.text)

            # Вопрос №2 - Сумма кредита
            await message.answer('Введите сумму кредита:', reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.M_credit_sum)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'M_credit_period'")
        await message.answer("Произошла ошибка. Попробуйте позже.")


# Обработка вопроса №2 - Сумма кредита
@micro_loan_router.message(F.text, Form.M_credit_sum)
async def M_credit_sum(message: Message, state: FSMContext):
    try:
        sum = ''.join(re.findall(r'\d+', message.text))
        await state.update_data(M_credit_sum=sum)

        # Вопрос №4 - Размер первого депозита
        await message.answer("Первоначальный взнос кредита дложен составлять 50% от оценочной стоимости дома или квартиры")
        await message.answer("Имеется ли у вас имущество, подходящее под этот критерий?", reply_markup=kb_yn)
        await state.set_state(Form.CPZ_first_payment)
    except Exception as exception:
        logger.error(f"Ошибка при обработке сообщения {message.text}: {exception} в состоянии 'M_credit_sum'")
        await message.answer("Произошла ошибка. Попробуйте позже.")

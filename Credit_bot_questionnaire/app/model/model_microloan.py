from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    M_credit_period = State()  # 1
    M_credit_sum = State()     # 2

    first_payment = State()                  # 4 
    reduce_credit_sum_or_autoloan = State()  # 4.1

    finish = State()
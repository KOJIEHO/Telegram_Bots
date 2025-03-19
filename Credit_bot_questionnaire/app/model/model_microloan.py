from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    apartment_or_house = State()  # 1
    credit_period = State()       # 2
    credit_sum = State()          # 3

    first_payment = State()                  # 4 
    reduce_credit_sum_or_autoloan = State()  # 4.1

    finish = State()
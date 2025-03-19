from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    CPZ_credit_type = State()         # 0
    CPZ_apartment_or_house = State()  # 1
    CPZ_credit_period = State()       # 2
    CPZ_credit_sum = State()          # 3

    CPZ_first_payment = State()                  # 4 
    CPZ_reduce_credit_sum_or_autoloan = State()  # 4.1

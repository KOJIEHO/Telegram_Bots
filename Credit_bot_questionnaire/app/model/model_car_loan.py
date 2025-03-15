from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    CL_credit_type = State()  # 1
    CL_is_rezident = State()  # 2
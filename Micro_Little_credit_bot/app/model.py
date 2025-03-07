from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    name = State()
    get_phone_number = State()
    approval = State()
    pay_done = State()

    credit_history_done = State()

    finish = State()

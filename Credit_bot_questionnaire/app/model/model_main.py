from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    credit_type = State()    # 1
    ipoteka_type = State()   # 1.1
    credit_period = State()  # 1.2
    credit_sum = State()     # 1.3
    first_payment = State()  # 1.4

    region = State()         # 2

    is_rezident = State()    # 3
    registration = State()   # 3.1

    is_сriminal_record = State()      # 4
    сriminal_record_econom = State()  # 4.1

    fssp = State()           # 5

    bank_salary = State()    # 6
    bank_name = State()      # 6.1

    credit_rating = State()  # 7


    test = State()


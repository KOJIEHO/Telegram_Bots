from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    CPZ_credit_type = State()         # 0
    CPZ_apartment_or_house = State()  # 1
    CPZ_credit_period = State()       # 2
    CPZ_credit_sum = State()          # 3
    CPZ_first_payment = State()                  # 4 
    CPZ_reduce_credit_sum_or_autoloan = State()  # 4.1

    # Общие состояния из анкеты
    CPZ_region = State()         # 5
    CPZ_is_rezident = State()    # 6
    CPZ_registration = State()   # 6.1

    CPZ_is_сriminal_record = State()      # 7
    CPZ_сriminal_record_econom = State()  # 7.1

    CPZ_fssp = State()           # 8

    CPZ_bank_salary = State()    # 9
    CPZ_bank_name = State()      # 9.1

# Потом доделать это, опка вообще не понимаю че там с финансово нагрузкой
    CPZ_credit_rating = State()        # 10
    CPZ_credit_rating_PDF = State()    # 10.1
    CPZ_credit_rating_write = State()  # 10.2
    # Считаем финансовую нагрузку
    CPZ_FB_credit = State()   # 10.3
# ------------------------------------

    CPZ_delay = State()   # 
    CPZ_birthday = State()   # 
    CPZ_family_status = State()   # 
    CPZ_salary_proof = State()   #
    CPZ_salary_type = State()   #
    CPZ_salary_size = State()   #
    CPZ_work_experience = State()   #
    CPZ_education = State()
    CPZ_borrower = State()


from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    CPZ_credit_type = State()             # 1   - Вид кредита

    # Вопросы характерные только для этого вида кредита
    CPZ_apartment_or_house = State()
    CPZ_credit_period = State()
    CPZ_credit_sum = State()
    CPZ_first_payment = State()  
    CPZ_reduce_credit_sum_or_autoloan = State()

    # Общие состояния из анкеты
    CPZ_region = State()                  # 2   - Регион
    CPZ_is_rezident = State()             # 3   - Резидент РФ
    CPZ_registration = State()            # 3.1 - Вид на жительство и регистрация 
    CPZ_is_сriminal_record = State()      # 4   - Судимость
    CPZ_сriminal_record_econom = State()  # 4.1 - Экономическая ли статья
    CPZ_fssp = State()                    # 5   - ФССП
    CPZ_bank_salary = State()             # 6   - Зарплатник банка
    CPZ_bank_name = State()               # 6.1 - Какой банк


    CPZ_credit_rating = State()           # 7   - Кредитная история
    CPZ_credit_rating_PDF = State()       # 7.1 - 
    CPZ_credit_rating_write = State()     # 7.2
# Потом доделать это, пока вообще не понимаю че там с финансово нагрузкой
    # Считаем финансовую нагрузку
    CPZ_FB_credit = State()               # 8.1
# ------------------------------------

    CPZ_delay = State()                   # 9    - Есть ли действующая просрочка
    CPZ_birthday = State()                # 10   - Дата рождения
    CPZ_family_status = State()           # 11   - Семейное положение
    CPZ_number_of_children = State()      # 12   - Кол-во детей
    CPZ_childrens_birthdays = State()     # 13   - Даты рождения детей
    CPZ_child_birthday = State()          # Для сбора даты рождения
    CPZ_current_child_index = State()     # Для отслеживания текущего ребенка  


    CPZ_is_izdiventsi = State()           # 14   - Иждивенцы
    CPZ_salary_proof = State()            # Есть ли подтверждение ЗП
    CPZ_salary_type = State()             # 15   - Тип ЗП
    CPZ_salary_size = State()             # 15.1 - Сумма ЗП
    CPZ_work_experience = State()         # 16   - Стаж работы
    CPZ_education = State()               # 18   - Образование
    CPZ_borrower = State()                # 20   - Являетесь ли созаемщиком


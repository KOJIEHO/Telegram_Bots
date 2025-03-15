from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_yn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да")],
        [KeyboardButton(text="Нет")]
    ],
    resize_keyboard=True
)

# kb_pay_done = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="✅Консультацию оплатил")]
#     ],
#     resize_keyboard=True
# )

# kb_file_done = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="✅Все верно")]
#     ],
#     resize_keyboard=True
# )

# kb_finish = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="✅Отправил")]
#     ],
#     resize_keyboard=True
# )

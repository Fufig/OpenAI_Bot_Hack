from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔥 Готов ответить на 3 вопроса! 🔥")],
        ],
        resize_keyboard=True
    )

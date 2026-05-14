from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Профиль'), KeyboardButton(text='Корзина')],
            [KeyboardButton(text='Каталог'), KeyboardButton(text='О Нас')],
        ],
        resize_keyboard=True,
    )
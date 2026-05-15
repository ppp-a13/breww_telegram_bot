from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def profile_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text='Пополнить баланс',
            callback_data='deposit'
        ),
        ]
    ])


def break_action_and_back_to_main_menu(text: str = 'Отменить'):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=text,
            callback_data='cancel_deposit'
        ),
        ]
    ])


def apply_deposit_action():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Да',
                callback_data='apply_deposit'
            ),
            InlineKeyboardButton(
                text='Нет',
                callback_data='cancel_deposit'
            )
        ]
    ])

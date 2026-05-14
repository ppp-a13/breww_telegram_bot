from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData


class CategoryCallBackData(CallbackData, prefix='category'):
    category_id: int


class TeasCallBackData(CallbackData, prefix='tea'):
    id: int

class BuyTeaCallBackData(CallbackData, prefix='buy_tea'):
    id: int

class CartCallBackData(CallbackData, prefix='cart'):
    tea_id: int
    action: str

class TeaPageCallBackData(CallbackData, prefix='tea_page'):
    category_id: int
    page: int

TEA_PER_PAGE = 5

def generate_catalog_keyboard(categories):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for category in categories:
        keyboard.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=category.name,
                    callback_data=CategoryCallBackData(category_id=category.id).pack()
                )
            ]
        )

    return keyboard

def generate_teas_callback(teas, category_id: int, page: int = 0):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    start = page * TEA_PER_PAGE
    end = start + TEA_PER_PAGE
    page_teas = teas[start:end]

    for tea in page_teas:
        keyboard.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=tea.name,
                    callback_data=TeasCallBackData(id=tea.id).pack()
                )
            ]
        )

    navigation_buttons = []
    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(
            text='<-',
            callback_data=TeaPageCallBackData(category_id=category_id, page=page - 1).pack()
        ))
    if end < len(teas):
        navigation_buttons.append(InlineKeyboardButton(
            text='>>',
            callback_data=TeaPageCallBackData(category_id=category_id, page=page + 1).pack()
        ))
    if navigation_buttons:
        keyboard.inline_keyboard.append(navigation_buttons)

    keyboard.inline_keyboard.append(
        [
            InlineKeyboardButton(text='<< Назад', callback_data='catalog')
        ]
    )

    return keyboard

def back_to_category_teas(tea_id, category_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='В корзину',
                    callback_data=CartCallBackData(tea_id=tea_id, action='add').pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text='<< Назад',
                    callback_data=CategoryCallBackData(category_id=category_id).pack()
                )
            ]
        ]
    )
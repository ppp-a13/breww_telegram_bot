from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

class AdminTeaCallBack(CallbackData, prefix='admin_tea'):
    tea_id: int
    action: str

class AdminEditFieldCallBack(CallbackData, prefix='admin_edit'):
    tea_id: int
    field: str

def admin_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Товары'), KeyboardButton(text='Пользователи')],
            [KeyboardButton(text='Выйти из админки')]
        ],
        resize_keyboard=True
    )


def admin_tea_list_keyboard(teas):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for tea in teas:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=tea.name,
                callback_data=AdminTeaCallBack(tea_id=tea.id, action='edit').pack()
            ),
            InlineKeyboardButton(
                text='Удалить',
                callback_data=AdminTeaCallBack(tea_id=tea.id, action='delete').pack()
            )
        ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='+ Добавить товар', callback_data='admin_add_tea')
    ])
    return keyboard

def admin_tea_edit_keyboard(tea_id):
    fields = [('Название', 'name'), ('Описание', 'description'), ('Цена', 'price'), ('Количество', 'quantity'), ('Фото', 'photo')]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for label, field in fields:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=f'Изменить {label}',
                callback_data=AdminEditFieldCallBack(tea_id=tea_id, field=field).pack()
            )
        ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='<< Назад', callback_data='admin_teas')
    ])
    return keyboard
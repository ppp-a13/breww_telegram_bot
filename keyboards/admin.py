from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

ADMIN_TEAS_PER_PAGE = 10


class AdminTeaCallBack(CallbackData, prefix='admin_tea'):
    tea_id: int
    action: str


class AdminEditFieldCallBack(CallbackData, prefix='admin_edit'):
    tea_id: int
    field: str


class AdminCategoryCallBack(CallbackData, prefix='admin_category'):
    category_id: int


class AdminTeaPageCallBack(CallbackData, prefix='admin_tea_page'):
    category_id: int
    page: int


def admin_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Товары'), KeyboardButton(text='Поиск пользователя')],
            [KeyboardButton(text='Выход из панели администратора')]
        ],
        resize_keyboard=True
    )


def admin_category_list_keyboard(categories):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for category in categories:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=category.name,
                callback_data=AdminCategoryCallBack(category_id=category.id).pack()
            )
        ])
    return keyboard


def admin_tea_list_keyboard(teas, category_id: int, page: int = 0):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    start = page * ADMIN_TEAS_PER_PAGE
    end = start + ADMIN_TEAS_PER_PAGE
    page_teas = teas[start:end]

    for tea in page_teas:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=tea.name,
                callback_data=AdminTeaCallBack(tea_id=tea.id, action='edit').pack()
            ),
            InlineKeyboardButton(
                text='УДАЛИТЬ',
                callback_data=AdminTeaCallBack(tea_id=tea.id, action='delete').pack()
            )
        ])

    navigation_buttons = []

    if page > 0:
        navigation_buttons.append(InlineKeyboardButton(
            text='◀️',
            callback_data=AdminTeaPageCallBack(category_id=category_id, page=page - 1).pack()
        ))
    if end < len(teas):
        navigation_buttons.append(InlineKeyboardButton(
            text='▶️',
            callback_data=AdminTeaPageCallBack(category_id=category_id, page=page + 1).pack()
        ))
    if navigation_buttons:
        keyboard.inline_keyboard.append(navigation_buttons)

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='ДОБАВИТЬ ТОВАР', callback_data='admin_add_tea')
    ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='НАЗАД В КАТЕГОРИИ', callback_data='admin_teas')
    ])
    return keyboard


def admin_tea_edit_keyboard(tea_id):
    fields = [
        ('Название', 'name'),
        ('Описание', 'description'),
        ('Стоимость', 'price'),
        ('Количество', 'quantity'),
        ('Фото', 'photo'),
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for label, field in fields:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text=label,
                callback_data=AdminEditFieldCallBack(tea_id=tea_id, field=field).pack()
            )
        ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='НАЗАД В КАТЕГОРИИ', callback_data='admin_teas')
    ])
    return keyboard

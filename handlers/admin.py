from aiogram import F, Router, types, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import ReplyKeyboardRemove

from filters.admin import IsAdmin
from keyboards.admin import *
from keyboards.menu import *
from repositories.teas import TeaRepository
from repositories.categories import CategoryRepository
from repositories.user import UserRepository
from states.admin import AddTeaStates, EditTeaState


router = Router()

@router.message(IsAdmin(), Command('admin'))
async def admin_panel(message: types.Message):
    await message.answer('Панель админа', reply_markup=admin_main_keyboard())

@router.message(IsAdmin(), F.text == 'Выйти из админки')
async def admin_exit(message: types.Message):
    await message.answer(
        'Вы вышли из панели администратора',
        reply_markup=main_menu_keyboard()
    )

@router.message(IsAdmin(), F.text == 'Товары')
@router.callback_query(IsAdmin(), F.data == 'admin_teas')
async def admin_teas(update: types.Message | types.CallbackQuery, tea_repository: TeaRepository):
    teas = list(await tea_repository.get_all_teas())
    text = f'Всего товаров: {len(teas)}'
    keyboard = admin_tea_list_keyboard(teas)
    if isinstance(update, types.Message):
        await update.answer(text, reply_markup=keyboard)
    else:
        await update.message.edit_text(text, reply_markup=keyboard)

@router.callback_query(IsAdmin(), AdminTeaCallBack.filter(F.action == 'delete'))
async def admin_delete_tea(callback: types.CallbackQuery, callback_data: AdminTeaCallBack, tea_repository: TeaRepository):
    await tea_repository.delete_tea(callback_data.tea_id)
    await callback.answer('Товар удален')
    teas = list(await tea_repository.get_all_teas())
    await callback.message.edit_text(f'Всего товаров: {len(teas)}', reply_markup=admin_tea_list_keyboard(teas))

@router.callback_query(IsAdmin(), F.data == 'admin_add_tea')
async def admin_add_tea_start(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AddTeaStates.name)
    await callback.message.answer('Введите название товара:')

@router.message(IsAdmin(), AddTeaStates.name)
async def add_tea_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddTeaStates.description)
    await message.answer('Введите описание:')

@router.message(IsAdmin(), AddTeaStates.description)
async def add_tea_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddTeaStates.price)
    await message.answer('Введите цену копейках:')

@router.message(IsAdmin(), AddTeaStates.price)
async def add_tea_price(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Цена должна быть числом, введите еще раз')
        return
    await state.update_data(price=int(message.text))
    await state.set_state(AddTeaStates.category_id)
    await message.answer('Введите ID категории:')

@router.message(IsAdmin(), AddTeaStates.category_id)
async def add_tea_category(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('ID должен быть числом:')
        return
    await state.update_data(category_id=int(message.text))
    await state.set_state(AddTeaStates.quantity)
    await message.answer('Введите количество:')

@router.message(IsAdmin(), AddTeaStates.quantity)
async def add_tea_quantity(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Количество должно быть числом:')
        return
    await state.update_data(quantity=int(message.text))
    await state.set_state(AddTeaStates.photo)
    await message.answer('Отправьте фото товара (или напишите "пропустить"):')

@router.message(IsAdmin(), AddTeaStates.photo, F.photo)
async def add_tea_photo(message: types.Message, state: FSMContext, tea_repository: TeaRepository):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    await _finish_add_tea(message, state, tea_repository)

@router.message(IsAdmin(), AddTeaStates.photo, F.text.lower() == 'пропустить')
async def add_tea_skip_photo(message: types.Message, state: FSMContext, tea_repository: TeaRepository):
    await state.update_data(photo_id=None)
    await _finish_add_tea(message, state, tea_repository)

async def _finish_add_tea(message: types.Message, state: FSMContext, tea_repository: TeaRepository):
    data = await state.get_data()
    await tea_repository.add_tea(**data)
    await state.clear()
    await message.answer(f'Товар «{data["name"]}» добавлен!')

@router.callback_query(IsAdmin(), AdminTeaCallBack.filter(F.action == 'edit'))
async def admin_edit_tea(callback: types.CallbackQuery, callback_data: AdminTeaCallBack, tea_repository: TeaRepository):
    tea = await tea_repository.get_tea_by_id(callback_data.tea_id)
    await callback.message.edit_text(
        f'Редактирование: {tea.name}\nЧто изменить?',
        reply_markup=admin_tea_edit_keyboard(callback_data.tea_id)
    )

@router.callback_query(IsAdmin(), AdminEditFieldCallBack.filter())
async def admin_edit_field(callback: types.CallbackQuery, callback_data: AdminEditFieldCallBack, state: FSMContext):
    await state.set_state(EditTeaState.new_value)
    await state.update_data(tea_id=callback_data.tea_id, field=callback_data.field)
    if callback_data.field == 'photo':
        await callback.message.answer('Отправьте новое фото:')
    else:
        await callback.message.answer(f'Введите новое значение для поля «{callback_data.field}»:')

@router.message(IsAdmin(), EditTeaState.new_value, F.photo)
async def admin_tea_field_photo(message: types.Message, state: FSMContext, tea_repository: TeaRepository):
    data = await state.get_data()
    await tea_repository.update_tea_fields(data['tea_id'], 'photo_id', message.photo[-1].file_id)
    await state.clear()
    await message.answer('Фото обновлено!')

@router.message(IsAdmin(), EditTeaState.new_value)
async def edit_tea_field_text(message: types.Message, state: FSMContext, tea_repository: TeaRepository):
    data = await state.get_data()
    field = data['field']
    value = message.text
    if field in ('price', 'quantity', 'category_id'):
        if not value.isdigit():
            await message.answer('Должно быть число, введите еще раз')
            return
        value = int(value)
    await tea_repository.update_tea_fields(data['tea_id'], field, value)
    await state.clear()
    await message.answer('Обновлено!')

@router.message(IsAdmin(), F.text == 'Пользователи')
async def admin_users(message: types.Message):
    await message.answer('Введите тг ID пользователя:')

@router.message(IsAdmin(), StateFilter(default_state), F.text.regexp(r'^\d+$'))
async def admin_find_user(message: types.Message, user_repository: UserRepository):
    user = await user_repository.get_by_telegram_id(int(message.text))
    if not user:
        await message.answer('Пользователь не найден')
        return
    await message.answer(
        f'ID: {user.telegram_id}\n'
        f'Username: @{user.username or "нет"}\n'
        f'Имя: {user.fullname}\n'
        f'Баланс: {user.view_balance}\n'
    )
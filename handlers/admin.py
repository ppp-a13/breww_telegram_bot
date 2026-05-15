from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from filters.admin import IsAdmin
from keyboards.admin import *
from keyboards.menu import *
from repositories.categories import CategoryRepository
from repositories.teas import TeaRepository
from repositories.user import UserRepository
from states.admin import AddTeaStates, EditTeaState

router = Router()

FIELD_NAMES = {
    'name': 'Название',
    'description': 'Описание',
    'price': 'Цена (в копейках)',
    'quantity': 'Количество',
    'category_id': 'ID категории',
}


@router.message(IsAdmin(), Command('admin'))
async def admin_panel(message: types.Message):
    await message.answer('Вы вошли в панель администратора', reply_markup=admin_main_keyboard())


@router.message(IsAdmin(), F.text == 'Выход из панели администратора')
async def admin_exit(message: types.Message):
    await message.answer(
        'Вы вышли из панели администратора',
        reply_markup=main_menu_keyboard()
    )


@router.message(IsAdmin(), F.text == 'Товары')
@router.callback_query(IsAdmin(), F.data == 'admin_teas')
async def admin_teas(update: types.Message | types.CallbackQuery, category_repository: CategoryRepository):
    categories = list(await category_repository.get_list())
    text = 'Выберите категорию:'
    keyboard = admin_category_list_keyboard(categories)
    if isinstance(update, types.Message):
        await update.answer(text, reply_markup=keyboard)
    else:
        await update.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(IsAdmin(), AdminCategoryCallBack.filter())
async def admin_category_teas(
        callback: types.CallbackQuery,
        callback_data: AdminCategoryCallBack,
        tea_repository: TeaRepository,
        category_repository: CategoryRepository
):
    category = await category_repository.get_by_id(callback_data.category_id)
    teas = await tea_repository.get_all_teas_by_category(callback_data.category_id)
    text = f'<b>{category.name}</b> — {len(teas)} товаров'
    await callback.message.edit_text(text,
                                     reply_markup=admin_tea_list_keyboard(teas, callback_data.category_id, page=0),
                                     parse_mode='html')
    await callback.answer()


@router.callback_query(IsAdmin(), AdminTeaPageCallBack.filter())
async def admin_tea_page(
        callback: types.CallbackQuery,
        callback_data: AdminTeaPageCallBack,
        tea_repository: TeaRepository,
        category_repository: CategoryRepository
):
    category = await category_repository.get_by_id(callback_data.category_id)
    teas = await tea_repository.get_all_teas_by_category(callback_data.category_id)
    text = f'<b>{category.name}</b> — {len(teas)} товаров'
    await callback.message.edit_text(text, reply_markup=admin_tea_list_keyboard(teas, callback_data.category_id,
                                                                                callback_data.page), parse_mode='html')
    await callback.answer()


@router.callback_query(IsAdmin(), AdminTeaCallBack.filter(F.action == 'delete'))
async def admin_delete_tea(callback: types.CallbackQuery, callback_data: AdminTeaCallBack,
                           tea_repository: TeaRepository, category_repository: CategoryRepository):
    tea = await tea_repository.get_tea_by_id(callback_data.tea_id)
    category_id = tea.category_id
    await tea_repository.delete_tea(callback_data.tea_id)
    await callback.answer('Товар удален')
    category = await category_repository.get_by_id(category_id)
    teas = await tea_repository.get_all_teas_by_category(category_id)
    await callback.message.edit_text(
        f'<b>{category.name}</b> — {len(teas)} товаров',
        reply_markup=admin_tea_list_keyboard(teas, category_id, page=0),
        parse_mode='html'
    )


@router.callback_query(IsAdmin(), F.data == 'admin_add_tea')
async def admin_add_tea_start(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AddTeaStates.name)
    await callback.message.answer('Введите название:')


@router.message(IsAdmin(), AddTeaStates.name)
async def add_tea_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddTeaStates.description)
    await message.answer('Введите описание:')


@router.message(IsAdmin(), AddTeaStates.description)
async def add_tea_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddTeaStates.price)
    await message.answer('Введите цену (в копейках):')


@router.message(IsAdmin(), AddTeaStates.price)
async def add_tea_price(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Кажется, цена некорректная. Попробуйте еще раз')
        return
    await state.update_data(price=int(message.text))
    await state.set_state(AddTeaStates.category_id)
    await message.answer('Введите ID категории:')


@router.message(IsAdmin(), AddTeaStates.category_id)
async def add_tea_category(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Кажется, ID некорректный. Попробуйте еще раз')
        return
    await state.update_data(category_id=int(message.text))
    await state.set_state(AddTeaStates.quantity)
    await message.answer('Введите количество:')


@router.message(IsAdmin(), AddTeaStates.quantity)
async def add_tea_quantity(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Кажется, число некорректно. Попробуйте еще раз')
        return
    await state.update_data(quantity=int(message.text))
    await state.set_state(AddTeaStates.photo)
    await message.answer('Отправьте фото товара (или напишите «пропустить»):')


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
    await message.answer(f'Товар «{data["name"]}» добавлен')


@router.callback_query(IsAdmin(), AdminTeaCallBack.filter(F.action == 'edit'))
async def admin_edit_tea(callback: types.CallbackQuery, callback_data: AdminTeaCallBack, tea_repository: TeaRepository):
    tea = await tea_repository.get_tea_by_id(callback_data.tea_id)
    await callback.message.edit_text(
        f'<b>Редактирование:</b> {tea.name}\n\nВыберите поле для изменения:',
        reply_markup=admin_tea_edit_keyboard(callback_data.tea_id),
        parse_mode='html'
    )


@router.callback_query(IsAdmin(), AdminEditFieldCallBack.filter())
async def admin_edit_field(callback: types.CallbackQuery, callback_data: AdminEditFieldCallBack, state: FSMContext):
    await state.set_state(EditTeaState.new_value)
    await state.update_data(tea_id=callback_data.tea_id, field=callback_data.field)
    if callback_data.field == 'photo':
        await callback.message.answer('Отправьте новое фото:')
    else:
        label = FIELD_NAMES.get(callback_data.field, callback_data.field)
        await callback.message.answer(f'Введите новое значение для «{label}»:')


@router.message(IsAdmin(), EditTeaState.new_value, F.photo)
async def admin_tea_field_photo(message: types.Message, state: FSMContext, tea_repository: TeaRepository):
    data = await state.get_data()
    await tea_repository.update_tea_fields(data['tea_id'], 'photo_id', message.photo[-1].file_id)
    await state.clear()
    await message.answer('Обновлено')


@router.message(IsAdmin(), EditTeaState.new_value)
async def edit_tea_field_text(message: types.Message, state: FSMContext, tea_repository: TeaRepository):
    data = await state.get_data()
    field = data['field']
    value = message.text
    if field in ('price', 'quantity', 'category_id'):
        if not value.isdigit():
            await message.answer('Кажется, число некорректное. Попробуйте еще раз')
            return
        value = int(value)
    await tea_repository.update_tea_fields(data['tea_id'], field, value)
    await state.clear()
    await message.answer('Обновлено')


@router.message(IsAdmin(), F.text == 'Поиск пользователя')
async def admin_users(message: types.Message):
    await message.answer('Введите Telegram ID пользователя:')


@router.message(IsAdmin(), StateFilter(default_state), F.text.regexp(r'^\d+$'))
async def admin_find_user(message: types.Message, user_repository: UserRepository):
    user = await user_repository.get_by_telegram_id(int(message.text))
    if not user:
        await message.answer('Пользователь не найден')
        return
    await message.answer(
        f'ID: {user.telegram_id}\n'
        f'Username: @{user.username or "отсутствует"}\n'
        f'Имя: {user.fullname}\n'
        f'Баланс: {user.view_balance}\n'
    )

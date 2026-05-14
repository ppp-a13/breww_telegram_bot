from aiogram import F, Router, types

from filters.check_buy_item import FilterUserCanBuyTea
from keyboards.catalog import generate_catalog_keyboard, CategoryCallBackData, generate_teas_callback, TeasCallBackData, \
    back_to_category_teas, BuyTeaCallBackData
from repositories.categories import CategoryRepository
from repositories.teas import TeaRepository
from repositories.user import UserRepository
from keyboards.catalog import TeaPageCallBackData

router = Router()


@router.callback_query(F.data == 'catalog')
@router.message(F.text == 'Каталог')
async def catalog(update: types.Message | types.CallbackQuery, category_repository: CategoryRepository):
    categories = await category_repository.get_list()

    if isinstance(update, types.Message):
        await update.answer(
            'Наш каталог:',
            reply_markup=generate_catalog_keyboard(categories)
        )
    else:
        await update.message.edit_text(
            'Наш каталог:',
            reply_markup=generate_catalog_keyboard(categories)
        )


@router.callback_query(CategoryCallBackData.filter())
async def category_info(
        callback: types.CallbackQuery,
        callback_data: CategoryCallBackData,
        category_repository: CategoryRepository,
        tea_repository: TeaRepository
):
    category = await category_repository.get_by_id(callback_data.category_id)
    teas = await tea_repository.get_teas_by_category_id(callback_data.category_id)
    keyboard = generate_teas_callback(teas, callback_data.category_id, page=0)

    if callback.message.photo:
        await callback.message.delete()
        await callback.message.answer(
            text=category.description,
            reply_markup=keyboard
        )
    else:
        await callback.message.edit_text(
            text=category.description,
            reply_markup=keyboard
        )

    await callback.answer()

@router.callback_query(TeasCallBackData.filter())
async def teas_info(callback: types.CallbackQuery, callback_data: TeasCallBackData, tea_repository: TeaRepository):
    tea = await tea_repository.get_tea_by_id(callback_data.id)

    text = (
        f'<b>{tea.name}</b>\n\n'
        f'{tea.description}\n\n'
        f'Стоимость {round(tea.price / 100, 2)} монеток'
    )
    keyboard = back_to_category_teas(tea.id, tea.category_id)

    if tea.photo_id:
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=tea.photo_id,
            caption=text,
            parse_mode='html',
            reply_markup=keyboard
        )
    else:
        await callback.message.edit_text(
            text,
            parse_mode='html',
            reply_markup=keyboard
        )

    await callback.answer()

@router.callback_query(FilterUserCanBuyTea(), BuyTeaCallBackData.filter())
async def buy_tea_action(
        callback: types.CallbackQuery,
        callback_data: BuyTeaCallBackData,
        tea_repository: TeaRepository,
        user_repository: UserRepository
):
    tea = await tea_repository.get_tea_by_id(callback_data.id)
    await user_repository.update_balance(callback.from_user.id, -tea.price)

    await callback.message.answer(
        f'Вы успешно купили {tea.name}!'
    )
    await callback.answer()

@router.callback_query(TeaPageCallBackData.filter())
async def tea_page(
        callback: types.CallbackQuery,
        callback_data: TeaPageCallBackData,
        category_repository: CategoryRepository,
        tea_repository: TeaRepository
):
    category = await category_repository.get_by_id(callback_data.category_id)
    teas =  await tea_repository.get_teas_by_category_id(callback_data.category_id)
    keyboard = generate_teas_callback(teas, callback_data.category_id, callback_data.page)

    await callback.message.edit_text(text=category.description, reply_markup=keyboard)
    await callback.answer()
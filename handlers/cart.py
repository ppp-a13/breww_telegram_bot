from aiogram import F, Router, types
from aiogram.utils import keyboard

from repositories.cart import CartRepository
from repositories.teas import TeaRepository
from repositories.user import UserRepository
from keyboards.catalog import CartCallBackData

router = Router()

@router.message(F.text == 'Корзина')
async def show_cart(message: types.Message, cart_repository: CartRepository, tea_repository: TeaRepository):
    items = list(await cart_repository.get_cart(message.from_user.id))

    if not items:
        await message.answer('Ваша корзина пуста')
        return

    text = 'Ваша корзина:\n\n'
    total = 0

    for item in items:
        tea = await tea_repository.get_tea_by_id(item.tea_id)
        item_total = tea.price * item.quantity
        total += item_total
        text += f'@ {tea.name} * {item.quantity} = {round(item_total / 100, 2)} монеток\n'

    text += f'\nИтого: {round(total / 100, 2)} монеток'

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Оформить заказ', callback_data='checkout')],
        [InlineKeyboardButton(text='Очистить корзину', callback_data='clear_cart')]
    ])

    await message.answer(text, reply_markup=keyboard)


@router.callback_query(CartCallBackData.filter(F.action == 'add'))
async def add_to_cart(
        callback: types.CallbackQuery,
        callback_data: CartCallBackData,
        cart_repository: CartRepository,
        tea_repository: TeaRepository
):
    tea = await tea_repository.get_tea_by_id(callback_data.tea_id)
    await cart_repository.add_item(callback.from_user.id, callback_data.tea_id)
    await callback.answer(f'"{tea.name}" добавлен в корзину!',show_alert=False)

@router.callback_query(F.data == 'clear_cart')
async def clear_cart(
        callback: types.CallbackQuery,
        cart_repository: CartRepository,
):
    await cart_repository.clear_cart(callback.from_user.id)
    await callback.message.edit_text('Корзина очищена', reply_markup=None)
    await callback.answer()


@router.callback_query(F.data == 'checkout')
async def checkout(
        callback: types.CallbackQuery,
        cart_repository: CartRepository,
        tea_repository: TeaRepository,
        user_repository: UserRepository
):
    items = list(await cart_repository.get_cart(callback.from_user.id))

    if not items:
        await callback.answer('Корзина пуста', show_alert=True)
        return

    total = 0

    for item in items:
        tea = await tea_repository.get_tea_by_id(item.tea_id)
        total += tea.price * item.quantity

    user = await user_repository.get_user_by_telegram_id(callback.from_user.id)

    if user.balance < total:
        await callback.answer(
            f'Недостаточно средств. Нужно {round(total / 100, 2)}, у Вас {user.view_balance}.',
            show_alert=True
        )
        return

    for item in items:
        tea = await tea_repository.get_tea_by_id(item.tea_id)
        new_quantity = max(0, tea.quantity - item.quantity)
        await tea_repository.update_tea_fields(item.tea_id, 'quantity', new_quantity)

    await user_repository.update_balance(callback.from_user.id, -total)
    await cart_repository.clear_cart(callback.from_user.id)

    await callback.message.edit_text('Заказ оформлен!')
    await callback.answer()
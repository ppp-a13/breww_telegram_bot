from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from keyboards import profile as profile_keyboard
from keyboards.catalog import BuyTeaCallBackData
from repositories.user import UserRepository
from states.profile import UserDepositState

router = Router()


@router.message(F.text == 'Профиль')
async def user_profile_information(
        message: types.Message,
        user_repository: UserRepository
):
    user = await user_repository.get_user_by_telegram_id(message.from_user.id)

    await message.answer(
        f'<b>{message.from_user.full_name}</b>\n'
        f'Username: @{user.username or 'отсутствует'}\n'
        f'ID: <code>{user.telegram_id}</code>\n'
        f'Ваш баланс: {user.view_balance} рублей',
        parse_mode=ParseMode.HTML,
        reply_markup=profile_keyboard.profile_menu()
    )


@router.callback_query(F.data == 'deposit')
async def user_deposit_action(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.edit_text(
        'Введите сумму пополнения:',
        reply_markup=profile_keyboard.break_action_and_back_to_main_menu()
    )
    await state.set_state(UserDepositState.INPUT_AMOUNT)


@router.callback_query(StateFilter(UserDepositState), F.data == 'cancel_deposit')
async def user_deposit_action_cancel(callback_query: types.CallbackQuery, state: FSMContext,
                                     user_repository: UserRepository):
    await state.clear()
    await callback_query.answer()

    user = await user_repository.get_user_by_telegram_id(callback_query.from_user.id)

    await callback_query.message.edit_text(
        f'<b>{callback_query.from_user.full_name}</b>\n'
        f'Username: @{user.username or 'отсутствует'}\n'
        f'ID: <code>{user.telegram_id}</code>\n'
        f'Ваш баланс: {user.view_balance} рублей',
        parse_mode=ParseMode.HTML,
        reply_markup=profile_keyboard.profile_menu()
    )


@router.message(UserDepositState.INPUT_AMOUNT)
async def user_deposit_amount(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Кажется, число некорректное. Попробуйте еще раз')
        return

    amount = int(message.text)

    await state.set_data({'amount': amount})
    await message.answer(
        f'Подтверждаете пополнение баланса на {amount} рублей?',
        reply_markup=profile_keyboard.apply_deposit_action()
    )
    await state.set_state(UserDepositState.APPLY_DEPOSIT)


@router.callback_query(UserDepositState.APPLY_DEPOSIT)
async def apply_user_deposit(
        callback_query: types.CallbackQuery, state: FSMContext, user_repository: UserRepository
):
    state_data = await state.get_data()
    deposit_amount = state_data.get('amount')

    await user_repository.update_balance(callback_query.from_user.id, deposit_amount * 100)
    await callback_query.message.edit_text(
        f'Баланс пополнен на {deposit_amount} рублей',
        reply_markup=profile_keyboard.break_action_and_back_to_main_menu(
            'Профиль'
        )
    )

    await callback_query.answer()


@router.callback_query(BuyTeaCallBackData.filter())
async def buy_tea_action(callback_query: types.CallbackQuery):
    await callback_query.answer()

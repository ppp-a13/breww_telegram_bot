from aiogram import Router, F, types


router = Router()

@router.message(F.text == 'О Нас')
async def info(message: types.Message):
    await message.answer(
        (
            'Я бот для покупки чая\n'
            'Ты можешь смотреть весь мой каталог и купить понравившийся чай.\n\n'
            'Хорошего чаепития!'
        )
    )
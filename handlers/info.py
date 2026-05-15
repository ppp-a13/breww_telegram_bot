from aiogram import Router, F, types

router = Router()


@router.message(F.text == 'О Нас')
async def info(message: types.Message):
    await message.answer(
        (
            'BREWW — небольшой магазин чая.\n\nМы отбираем чаи вручную: листовые, пуэры, улуны, белые и травяные сборы. Никакой пыли в пакетиках — только то, что стоит заваривать.'
        )
    )

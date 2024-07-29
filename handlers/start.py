from aiogram.filters import Command
from aiogram import Router, F, types

start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: types.Message):

    kb = types.InlineKeyboardMarkup(
    )
    await message.answer(
        text=f"Привет, {message.from_user.first_name},  я бот, который может оскорбить вас",
        reply_markup=kb
    )




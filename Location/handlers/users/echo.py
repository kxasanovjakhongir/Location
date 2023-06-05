from aiogram import types
from aiogram.types import reply_keyboard, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from loader import dp


#Echo bot
@dp.message_handler()
async def bot_echo(message: types.Message):
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Location', request_location=True)],
                  [KeyboardButton(text='/joylar_royxati')],],
        resize_keyboard=True, one_time_keyboard=True,
    )
    await message.answer("Boshqa locatsiya belgilashingiz mumkun!")
    await message.answer("---------------------------", reply_markup=menu)
    #await message.answer(message.text)

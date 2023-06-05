from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.types import reply_keyboard, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.builtin import CommandStart
import requests
import json
from aiogram.dispatcher.filters.state import State, StatesGroup
from loader import dp, bot
from states.nomlar import nomlar
from aiogram.dispatcher import FSMContext

lon = 0
lat = 0
joy = ''
fay_name = ''
token = ''
headers = {}
ls = []


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    global fay_name
    await message.answer(f"Salom, {message.from_user.full_name}!")
    await message.answer("Siz bu bot orqali,keyinroq kelmoqchi bo'lgan joylaringizni belgilap ketishingiz mumkin!\nBuning uchun sizdan Location tugmasini bosish talab qilinadi!")
    fay_name = str(message.from_user.id)+".txt"
    with open(fay_name, "a+"):
        print("Fayl")
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Location', request_location=True)],],
        resize_keyboard=True, one_time_keyboard=True,
    )
    await message.answer("---------------------------", reply_markup=menu)


@dp.message_handler(content_types='location')
async def loc(message: types.Message):
    global lon, lat
    lon = message.location.longitude
    lat = message.location.latitude
    loc = str(lon)+str('/')+str(lat)
    global token
    token = 'pk.c10da35656b614de98a3177ccac075e9'
    global headers
    headers = {"Accept-Language": "en"}
    address = requests.get(
        f'https://eu1.locationiq.com/v1/reverse.php?key={token}&lat={lat}&lon={lon}&format=json', headers=headers).json()
    adr = address['address']
    kocha = address['address']['road']
    shahar = address['address']['city']
    pchta = address['address']['postcode']
    res = address['address']['country']
    d_kod = address['address']['country_code']
    await message.answer(f"Siz xozirda \n{res} Respublikasi\n{shahar}ning\n{kocha}dasiz\nBu manzil pochta indexi {pchta}\nDavlat kodi {d_kod}")
    await message.answer("Bu joyga keyinchalik kelish kerak dep xisoblaysizmi")
    menu1 = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='XA')],
                  [KeyboardButton(text="Yo'q")]],
        resize_keyboard=True, one_time_keyboard=True,
    )
    await message.answer("---------------------------", reply_markup=menu1)


@dp.message_handler(text=["XA"])
async def xa(message: types.Message):
    await message.answer("Iltimos bu manzil uchun nom bering!")
    await nomlar.nom.set()
#############################################################

@dp.message_handler(text=["Yo'q"])
async def yoq(message: types.Message):
    menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Location', request_location=True)],
                  [KeyboardButton(text='/joylar_royxati')],],
        resize_keyboard=True, one_time_keyboard=True,
    )
    await message.answer("Boshqa locatsiya belgilashingiz mumkun!")
    await message.answer("---------------------------", reply_markup=menu)


@dp.message_handler(commands=["joylar_royxati"])
async def ruyxat(message: types.Message):
    inline_kb1 = InlineKeyboardMarkup()
    with open(fay_name, "r+")as f4:
        a = f4.readlines()
        for i in range(len(a)):
            st1 = a[i].split(";")[0]
            st = "/"+st1
            inline_btn_1 = InlineKeyboardButton(
                st.replace('/', ''), callback_data='button'+st)
            inline_kb1.add(inline_btn_1)

    a_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Location', request_location=True)]],
        resize_keyboard=True
    )
    await message.answer("--------------------", reply_markup=inline_kb1)


@dp.callback_query_handler(Text(startswith="button"))
async def process_callback_button1(callback_query: types.CallbackQuery):

    m = callback_query.data.split('/')[-1]
    with open(fay_name, "r+") as f5:
        a = f5.readlines()
        for i in range(len(a)):
            st = a[i].split(";")[0]
            # print(m, st)
            if m == st:
                lat1 = a[i].split(";")[1]
                lon1 = a[i].split(";")[2]
                address = requests.get(
                    f'https://eu1.locationiq.com/v1/reverse.php?key={token}&lat={lat1}&lon={lon1}&format=json', headers=headers).json()
                adr = address['address']
                kocha = address['address']['road']
                shahar = address['address']['city']
                pchta = address['address']['postcode']
                res = address['address']['country']
                d_kod = address['address']['country_code']
                await bot.send_message(callback_query.from_user.id, f"Siz qidirgan manzil \n{res} Respublikasi\n{shahar}ning\n{kocha}da\nBu manzil pochta indexi {pchta}\nDavlat kodi {d_kod}")
                await bot.send_location(callback_query.from_user.id, lat1, lon1)


@dp.message_handler(state=nomlar.nom)
async def el(message: types.Message, state: FSMContext):
    a = message.text
    with open(fay_name, "a+")as f2:
        f2.write(f"{a};{lat};{lon}\n")
        a_menu = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text='Boshqa Locatsia yuborish', request_location=True)],
                      [KeyboardButton(text='/joylar_royxati')]],
            resize_keyboard=True
        )
    global ls
    with open(fay_name, "r+")as f4:
        a = f4.readlines()
        for i in range(len(a)):
            st1 = a[i].split(";")[0]
            st = "/"+st1
            ls.append(st1.strip())
    await message.answer("Manzil saqlandi", reply_markup=a_menu)
    await state.finish()

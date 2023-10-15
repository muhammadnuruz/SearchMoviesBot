from aiogram import types
from aiogram.dispatcher.filters import Text

from bot.buttons.text import cabinet, vip, add_money, info, advert_and_support
from bot.dispatcher import dp


@dp.message_handler(Text(cabinet))
async def cabinet_function(msg: types.Message):
    await msg.answer(text=f"""
ℹ️ Malumotlaringiz:

🆔ID: {msg.from_user.id}
📝Ism-Familiya: {msg.from_user.full_name}
💰Balans: 0 uzs
""")


@dp.message_handler(Text(vip))
async def vip_function(msg: types.Message):
    await msg.answer(text=f"Balansda pul yetarli emas❗️")


@dp.message_handler(Text(add_money))
async def add_money_function(msg: types.Message):
    await msg.answer(text=f"Tez orada ishga tushadi❗️")


@dp.message_handler(Text(info))
async def add_info_function(msg: types.Message):
    await msg.answer(text=f"Tez orada ishga tushadi❗️")


@dp.message_handler(Text(advert_and_support))
async def add_advert_function(msg: types.Message):
    await msg.answer(text=f"Tez orada ishga tushadi❗️")

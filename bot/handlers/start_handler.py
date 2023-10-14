from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.reply_buttons import main_menu_buttons
from bot.buttons.text import back_main_menu
from bot.dispatcher import dp, bot
from db.model import User, Admins


@dp.message_handler(commands=['start'])
async def start_function(msg: types.Message):
    user = await User.get(str(msg.from_user.id))
    if user:
        await msg.answer(text=f"Assalomu alaykum {msg.from_user.first_name}", reply_markup=await main_menu_buttons())
    else:
        admins = await Admins.get_all()
        await User.create(chat_id=str(msg.from_user.id), fullname=msg.from_user.full_name,
                          username=msg.from_user.username)
        for admin in admins:
            await bot.send_message(chat_id=admin[0].chat_id,
                                   text=f"""
Yangi user🆕
ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>
Ism-Familiya: {msg.from_user.full_name}
Username: @{msg.from_user.username}""", parse_mode="HTML")
            await msg.answer(text=f"Assalomu alaykum {msg.from_user.first_name}",
                             reply_markup=await main_menu_buttons())


@dp.message_handler(Text(back_main_menu), state='*')
async def back_main_menu_function(msg: types.Message, state: FSMContext):
    await msg.answer(text=f"Assalomu alaykum {msg.from_user.first_name}", reply_markup=await main_menu_buttons())
    await state.finish()


@dp.callback_query_handler(Text(back_main_menu), state='*')
async def back_main_menu_function(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text=f"Assalomu alaykum {call.from_user.first_name}",
                              reply_markup=await main_menu_buttons())
    await state.finish()

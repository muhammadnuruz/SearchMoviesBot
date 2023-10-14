from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import sub_admins_button
from bot.buttons.reply_buttons import admin_buttons, back_main_menu_buttons, admins_buttons
from bot.buttons.text import admins_txt, statistic, sub_admins, add_admins
from bot.dispatcher import dp
from db.model import Admins, User


@dp.message_handler(commands='admin')
async def admin(msg: types.Message):
    admins = await Admins.get_all()
    for admin in admins:
        if str(msg.from_user.id) in admin[0].chat_id:
            await msg.answer(text=f"👨‍💻 Admin paneliga xush kelibsiz!", reply_markup=await admin_buttons())


@dp.message_handler(Text(statistic))
async def statistic(msg: types.Message):
    fuser = await User.get_all()
    await msg.answer(f"👥 Foydalanuvchilar soni: {len(fuser)}")


@dp.message_handler(Text(admins_txt))
async def admin_msg(msg: types.Message):
    k = 0
    admins = await Admins.get_all()
    reply = f"🧑‍💻 Adminlar soni {len(admins)}\n\n"
    for i in admins:
        k += 1
        reply += f"🆔 {k}-admin ID si) <a href='tg://user?id={i[0].chat_id}'>{i[0].chat_id}</a>\n"
    await msg.answer(text=reply, reply_markup=await admins_buttons(), parse_mode="HTML")


@dp.message_handler(Text(add_admins))
async def channel_add(msg: types.Message, state: FSMContext):
    await state.set_state('admin_id')
    await msg.answer(text=f"🆔 User ID sini yuboring ❗️ User botni ishlatgan bo'lishi zarur",
                     reply_markup=await back_main_menu_buttons())


@dp.message_handler(state='admin_id')
async def channel_id(msg: types.Message, state: FSMContext):
    user = await User.get(str(msg.text))
    if user:
        await Admins.create(chat_id=msg.text)
        await msg.answer(text=f"✅ Admin qo'shildi", reply_markup=await admin_buttons())
        await state.finish()
    else:
        await msg.answer(text=f"❗️ Bu user botni ishlatmagan\n🆔 User ID sini yuboring")


@dp.message_handler(Text(sub_admins))
async def channel_sub(msg: types.Message):
    await msg.answer(text=f"🪓 Qaysi adminni o'chirasiz", reply_markup=await sub_admins_button())


@dp.callback_query_handler(Text(startswith='admin'))
async def channel_sub_id(call: types.CallbackQuery):
    await Admins.delete(call.data.split("_")[1])
    await call.answer(text="✅ Admin o'chirib tashlandi")
    await call.message.edit_text(text=f"🪓 Qaysi adminni o'chirasiz", reply_markup=await sub_admins_button())

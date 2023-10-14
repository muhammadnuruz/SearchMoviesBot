from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import movies_buttons, get_name_movies_button, get_by_created_at_button, \
    get_id_movies_button, get_by_seen_button
from bot.buttons.reply_buttons import back_main_menu_buttons
from bot.buttons.text import movie, search_by_name, search_by_created_at, search_by_seen
from bot.dispatcher import dp
from db.model import Movies


@dp.message_handler(Text(movie))
async def movie_function(msg: types.Message):
    await msg.answer(text="Quidagilardan birini tanlang:", reply_markup=await movies_buttons())


@dp.callback_query_handler(Text(startswith='movie'))
async def get_movie_function(call: types.CallbackQuery):
    txt, id_ = call.data.split('_')
    id_ = int(id_)
    movies, button = await get_id_movies_button(id_=id_)
    await Movies.update(id_=id_, seen=movies[0].seen + 1)
    await call.message.delete()
    await call.message.answer_video(video=movies[0].path, caption=f"""
🎬 Nomi: {movies[0].name}
🌍 Davlati: {movies[0].country}
🇺🇿 Tili: {movies[0].language}
📆 Yili: {movies[0].date}
🎞 Janri: {movies[0].genre}
👁‍🗨 Ko'rilgan: {movies[0].seen}
    """, reply_markup=button)


@dp.callback_query_handler(Text(search_by_name))
async def search_by_name_function(call: types.CallbackQuery, state: FSMContext):
    await state.set_state('search_movie')
    await call.message.delete()
    await call.message.answer(text="Kino nomini yuboring:", reply_markup=await back_main_menu_buttons())


@dp.message_handler(state='search_movie')
async def search_by_name_function_2(msg: types.Message, state: FSMContext):
    movies, button = await get_name_movies_button(name=msg.text)
    if movies:
        await Movies.update(id_=movies[0].id, seen=movies[0].seen + 1)
        await msg.answer_video(video=movies[0].path, caption=f"""
🎬 Nomi: {movies[0].name}
🌍 Davlati: {movies[0].country}
🇺🇿 Tili: {movies[0].language}
📆 Yili: {movies[0].date}
🎞 Janri: {movies[0].genre}
👁‍🗨 Ko'rilgan: {movies[0].seen}
""", reply_markup=button)
        await state.finish()
    else:
        await msg.answer(text="Bunday kino topilmadi❗\nKino nomini yuboring:",
                         reply_markup=await back_main_menu_buttons())


@dp.callback_query_handler(Text(search_by_created_at))
async def search_by_created_at_function(call: types.CallbackQuery):
    button = await get_by_created_at_button(num=0)
    await call.message.delete()
    await call.message.answer(text="Eng so'ngi yuklangan kinolar:", reply_markup=button)


@dp.callback_query_handler(Text(startswith='next'))
async def get_movies_next_function(call: types.CallbackQuery):
    txt, id_ = call.data.split('_')
    button = await get_by_created_at_button(num=int(id_))
    await call.message.delete()
    await call.message.answer(text="Eng so'ngi yuklangan kinolar:", reply_markup=button)


@dp.callback_query_handler(Text(startswith='old'))
async def get_movies_old_function(call: types.CallbackQuery):
    txt, id_ = call.data.split('_')
    button = await get_by_created_at_button(num=int(id_))
    await call.message.delete()
    await call.message.answer(text="Eng so'ngi yuklangan kinolar:", reply_markup=button)


@dp.callback_query_handler(Text(search_by_seen))
async def sorted_by_seen_function(call: types.CallbackQuery):
    button = await get_by_seen_button(num=0)
    await call.message.delete()
    await call.message.answer(text="Eng ko'p ko'rilgan kinolar:", reply_markup=button)


@dp.callback_query_handler(Text(endswith='next'))
async def get_movies_next_function(call: types.CallbackQuery):
    id_, txt = call.data.split('_')
    button = await get_by_seen_button(num=int(id_))
    await call.message.delete()
    await call.message.answer(text="Eng ko'p ko'rilgan kinolar:", reply_markup=button)


@dp.callback_query_handler(Text(endswith='old'))
async def get_movies_old_function(call: types.CallbackQuery):
    id_, txt = call.data.split('_')
    button = await get_by_seen_button(num=int(id_))
    await call.message.delete()
    await call.message.answer(text="Eng ko'p ko'rilgan kinolar:", reply_markup=button)

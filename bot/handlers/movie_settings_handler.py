import uuid

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

from bot.buttons.inline_buttons import get_name_movies_button
from bot.buttons.reply_buttons import movies_settings_buttons, back_main_menu_buttons, admin_buttons
from bot.buttons.text import movie_setting, add_movie, sub_movie
from bot.dispatcher import dp, bot
from db.model import Movies


@dp.message_handler(Text(movie_setting))
async def movie_settings_function(msg: types.Message):
    await msg.answer(text="Kinolar bo'limi: ", reply_markup=await movies_settings_buttons())


@dp.message_handler(Text(add_movie))
async def add_movie_step_1(msg: types.Message, state: FSMContext):
    await state.set_state('movie_name')
    await msg.answer(text="Kino nomi:", reply_markup=await back_main_menu_buttons())


@dp.message_handler(state='movie_name')
async def add_movie_step_2(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
    await state.set_state('movie_country')
    await msg.answer(text="Kino davlati:")


@dp.message_handler(state='movie_country')
async def add_movie_step_3(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['country'] = msg.text
    await state.set_state('movie_language')
    await msg.answer(text="Kino tili:")


@dp.message_handler(state='movie_language')
async def add_movie_step_4(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['language'] = msg.text
    await state.set_state('movie_date')
    await msg.answer(text="Kino yili:")


@dp.message_handler(state='movie_date')
async def add_movie_step_5(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = msg.text
    await state.set_state('movie_genre')
    await msg.answer(text="Kino janri:")


@dp.message_handler(state='movie_genre')
async def add_movie_step_6(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['genre'] = msg.text
    await state.set_state('movie_path')
    await msg.answer(text="Kino:")


@dp.message_handler(state='movie_path', content_types=ContentType.VIDEO)
async def add_movie_step_7(msg: types.Message, state: FSMContext):
    async with state.proxy() as data: pass
    path = "movies/" + str(uuid.uuid4()) + "mp4"
    file = await bot.get_file(msg.video.file_id)
    await bot.download_file(file.file_path, f"{path}")
    await Movies.create(name=data['name'], path=path, country=data['country'], language=data['language'],
                        date=data['date'], genre=data['genre'])
    await state.finish()
    await msg.answer(text="Kino saqlandi✅", reply_markup=await admin_buttons())


@dp.message_handler(Text(sub_movie))
async def sub_movie_step_1(msg: types.Message, state: FSMContext):
    await state.set_state('sub_movie_name')
    await msg.answer(text='Kino nomini yuboring', reply_markup=await back_main_menu_buttons())


@dp.message_handler(state='sub_movie_name')
async def sub_movie_step_2(msg: types.Message, state: FSMContext):
    movies, button = await get_name_movies_button(name=msg.text)
    if movies:
        await Movies.delete(movies[0].id)
        await msg.answer(text=f"Kino o'chirildi", reply_markup=await admin_buttons())
        await state.finish()
    else:
        await msg.answer(text="Bunday kino topilmadi!\nKino nomini yuboring")

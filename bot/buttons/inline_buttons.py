from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.buttons.text import search_by_name, search_by_created_at, search_by_seen, back_main_menu, send_msg, \
    send_forward, send_user
from db.model import Movies, Admins


async def movies_buttons():
    design = [
        [InlineKeyboardButton(text=search_by_name, callback_data=search_by_name)],
        [InlineKeyboardButton(text=search_by_created_at, callback_data=search_by_created_at)],
        [InlineKeyboardButton(text=search_by_seen, callback_data=search_by_seen)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def get_name_movies_button(name: str):
    movies = await Movies.filter_by_name(name)
    if movies:
        design = [
            [InlineKeyboardButton(text=back_main_menu, callback_data=back_main_menu)]
        ]
        return movies, InlineKeyboardMarkup(inline_keyboard=design)
    else:
        return None, False


async def get_id_movies_button(id_: int):
    movies = await Movies.id_get(int(id_))
    design = [
        [InlineKeyboardButton(text=back_main_menu, callback_data=back_main_menu)]
    ]
    return movies, InlineKeyboardMarkup(inline_keyboard=design)


async def get_by_created_at_button(num: int):
    movies = await Movies.filter_by_created_at(num=num)
    design = []
    for movie in movies:
        design.append([InlineKeyboardButton(text=movie[0].name, callback_data=f"movie_{movie[0].id}")])
    if num == 0:
        design.append([InlineKeyboardButton(text='⏩', callback_data=f'next_{num + 10}')])
    elif len(movies) != 10:
        design.append([InlineKeyboardButton(text='⏪', callback_data=f'old_{num - 10}')])
    else:
        design.append(
            [InlineKeyboardButton(text='⏪', callback_data=f'old_{num - 10}'),
             InlineKeyboardButton(text='⏩', callback_data=f'next_{num + 10}')])
    return InlineKeyboardMarkup(inline_keyboard=design)


async def get_by_seen_button(num: int):
    movies = await Movies.filter_by_seen(num=num)
    design = []
    for movie in movies:
        design.append([InlineKeyboardButton(text=movie[0].name, callback_data=f"movie_{movie[0].id}")])
    if num == 0:
        design.append([InlineKeyboardButton(text='⏩', callback_data=f'{num + 10}_next')])
    elif len(movies) != 10:
        design.append([InlineKeyboardButton(text='⏪', callback_data=f'{num - 10}_old')])
    else:
        design.append(
            [InlineKeyboardButton(text='⏪', callback_data=f'{num - 10}_old'),
             InlineKeyboardButton(text='⏩', callback_data=f'{num + 10}_next')])
    return InlineKeyboardMarkup(inline_keyboard=design)


async def sub_admins_button():
    admins = await Admins.get_all()
    design = []
    for i in admins:
        design.append([InlineKeyboardButton(text=i[0].chat_id, callback_data="admin_" + i[0].chat_id)])
    return InlineKeyboardMarkup(inline_keyboard=design)


async def advert_buttons():
    design = [
        [InlineKeyboardButton(text=send_msg, callback_data=send_msg),
         InlineKeyboardButton(text=send_forward, callback_data=send_forward)],
        [InlineKeyboardButton(text=send_user, callback_data=send_user)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)

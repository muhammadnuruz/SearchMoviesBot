from aiogram.types import ReplyKeyboardMarkup

from bot.buttons.text import movie, back_main_menu, admins_txt, statistic, advert, sub_admins, add_admins, add_movie, \
    sub_movie, movie_setting


async def main_menu_buttons():
    design = [[movie]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def back_main_menu_buttons():
    design = [[back_main_menu]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def admin_buttons():
    design = [
        [statistic, admins_txt, movie_setting],
        [advert, back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def admins_buttons():
    design = [
        [add_admins, sub_admins],
        [back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def movies_settings_buttons():
    design = [
        [add_movie, sub_movie],
        [back_main_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)

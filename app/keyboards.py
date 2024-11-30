from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


### Кнопки внизу ###
kb_user = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Дай кота")]
],
    resize_keyboard=True)

kb_user_end = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Начать заново")]
],
    resize_keyboard=True)

kb_admin = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Дай кота"), KeyboardButton(text="Проверка")]
],
    resize_keyboard=True)

kb_admin_panel = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Вернуться")]
],
    resize_keyboard=True)
### Кнопки внизу ###


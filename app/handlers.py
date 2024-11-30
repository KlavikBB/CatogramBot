

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import (Message, CallbackQuery,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from sqlalchemy.orm.exc import UnmappedInstanceError

import app.keyboards as kb
from app.database.requests import *

import uuid

router = Router()

content_data_storage = {}

### Обработчики команд ###
@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user_status = await check_user(user_id)
    if user_status == 'admin':
        await message.answer(f"Приветствую тебя в боте с котами и не только", 
                            reply_markup=kb.kb_admin)
    else:
        await message.answer(f"Приветствую тебя в боте с котами и не только", 
                            reply_markup=kb.kb_user)
### Обработчики команд ###


### Обработчики текста ###
@router.message(F.text == "Дай кота")
async def give_cat_handler(message: Message):
    user_id = message.from_user.id
    content_data = await get_content(user_id)
    if content_data[1] == 'photo':
        await message.answer_photo(photo=f"{content_data[0]}")
    elif content_data[1] == 'video':
        await message.answer_video(video=f"{content_data[0]}")
    else:
        await message.answer("Больше ничего нет, начать заново?", reply_markup=kb.kb_user_end)

@router.message(F.text == "Начать заново")
async def end_handler(message: Message):
    user_id = message.from_user.id
    await reset_user_counter(user_id)
    user_status = await check_user(user_id)
    if user_status == 'admin':
        await message.answer(f"Готово, можем начать заново", 
                            reply_markup=kb.kb_admin)
    else:
        await message.answer(f"Готово, можем начать заново", 
                            reply_markup=kb.kb_user)


@router.message(F.text == "Проверка")
async def check_handler(message: Message):
    user_id = message.from_user.id
    user_status = await check_user(user_id)
    if user_status == 'admin':
        content_data = await get_content_to_approve()

        unique_id = str(uuid.uuid4())
        content_data_storage[unique_id] = content_data

        kb_admin_inline = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Добавить", callback_data=f"add_{unique_id}"), 
            InlineKeyboardButton(text="Удалить", callback_data=f"delete_{unique_id}")]
        ])

        if content_data[1] == 'photo':
            await message.answer_photo(photo=f"{content_data[0]}", 
                                        reply_markup=kb_admin_inline)
        elif content_data[1] == 'video':
            await message.answer_video(video=f"{content_data[0]}", 
                                        reply_markup=kb_admin_inline)
        else:
            await message.answer("Больше ничего нет", 
                                reply_markup=kb.kb_admin)
    else:
        await message.answer(f"?", 
                            reply_markup=kb.kb_user)

        
@router.message(F.text == "Вернуться")
async def back_handler(message: Message):
    user_id = message.from_user.id
    user_status = await check_user(user_id)
    if user_status == 'admin':
        await message.answer(f"Выбери пункт меню", 
                            reply_markup=kb.kb_admin)
    else:
        await message.answer(f"?", 
                            reply_markup=kb.kb_user)

### Обработчики текста ###    
    

### Обработчики фото и видео ###
@router.message(F.photo)
async def photo_handler(message: Message):
    await save_photo(f"{message.photo[-1].file_id}")

@router.message(F.video)
async def video_handler(message: Message):
    await save_video(f"{message.video.file_id}")
### Обработчики фото и видео ###

### Обработчики inline кнопок ###
@router.callback_query(lambda c: c.data.startswith('add_'))
async def add_handler(callback: CallbackQuery):
    _, unique_id = callback.data.split('_')
    content_data = content_data_storage.get(unique_id)

    try:
        if content_data[1] == "photo":
            await accept_photo(content_data[0])
            await callback.answer(f"Фотография добавлена в общий пул")
            await callback.message.delete_reply_markup()
        elif content_data[1] == "video":
            await accept_video(content_data[0])
            await callback.answer(f"Видео добавлено в общий пул")
            await callback.message.delete_reply_markup()
        else:
            await callback.answer(f"Произошла ошибка")
    except UnmappedInstanceError as e:
        await callback.answer(f"Запись уже удалена")
        await callback.message.delete_reply_markup()

    content_data_storage.pop(unique_id)

@router.callback_query(lambda c: c.data.startswith('delete_'))
async def delete_handler(callback: CallbackQuery):
    _, unique_id = callback.data.split('_')
    content_data = content_data_storage.get(unique_id)
    
    try:
        if content_data[1] == "photo":
            await delete_photo(content_data[0])
            await callback.answer(f"Фотография удалена{content_data}")
            await callback.message.delete_reply_markup()
        elif content_data[1] == "video":
            await delete_video(content_data[0])
            await callback.answer(f"Видео удалено{content_data}")
            await callback.message.delete_reply_markup()
        else:
            await callback.answer(f"Произошла ошибка")
    except UnmappedInstanceError as e:
        await callback.answer(f"Запись уже удалена")
        await callback.message.delete_reply_markup()
        

    content_data_storage.pop(unique_id)
### Обработчики inline кнопок ###
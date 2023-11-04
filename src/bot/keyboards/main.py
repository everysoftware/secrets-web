from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    Message,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.db import Database

MAIN_MENU_KB = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Хранилище 📁'),
            KeyboardButton(text='Мой профиль 👨'),
        ],
        [
            KeyboardButton(text='Добавить ⏬'),
            KeyboardButton(text='Сгенерировать 🔑')
        ]
    ],
    resize_keyboard=True,
    # one_time_keyboard=True
)


async def get_storage_kb(msg: Message, db: Database) -> InlineKeyboardMarkup:
    async with db.session.begin():
        user = await db.user.get(msg.from_user.id)
        records = user.records

    builder = InlineKeyboardBuilder()
    for record in records:
        builder.add(InlineKeyboardButton(text=record.title, callback_data=f'show_record_{record.id}'))
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


RECORD_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Изменить запись ✏️', callback_data='edit_record'),
            InlineKeyboardButton(text='Удалить запись ❌', callback_data='delete_record')
        ],
        [
            InlineKeyboardButton(text='Удалить сообщение ❎', callback_data='delete_msg_record')
        ],
    ]
)

YESNO_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да ✅', callback_data='yes'),
            InlineKeyboardButton(text='Нет ❌', callback_data='no')
        ]
    ]
)

UPDATE_RECORD_KB = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Имя веб-сайта', callback_data='update_title'),
            InlineKeyboardButton(text='Имя пользователя', callback_data='update_username'),

        ],
        [
            InlineKeyboardButton(text='Пароль', callback_data='update_password'),
            InlineKeyboardButton(text='Веб-сайт', callback_data='update_url'),
        ],
        [
            InlineKeyboardButton(text='Комментарий', callback_data='update_comment')
        ],
    ]
)

PROFILE_KB = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Сменить пароль 🔑'),
            KeyboardButton(text='Сменить мастер-пароль 🗝'),
        ],
        [
            KeyboardButton(text='Удалить аккаунт ❌'),
            KeyboardButton(text='Назад ◀️')
        ],
    ],
    resize_keyboard=True
)
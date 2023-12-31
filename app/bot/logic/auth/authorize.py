from aiogram import F, Router, types
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import joinedload

from app.bot import LoginGroup
from app.bot.logic.main import show_main_menu
from app.core import Database, User
from utils import DataVerification

router = Router()


@router.message(F.content_type == ContentType.WEB_APP_DATA, LoginGroup.type_password)
async def receive_credentials(
        message: types.Message, state: FSMContext, db: Database
) -> None:
    password = message.web_app_data.data
    async with db.session.begin():
        user = await db.user.get(
            message.from_user.id, options=[joinedload(User.credentials)]
        )

    if DataVerification.verify(
            password, user.credentials.password, user.credentials.salt
    ):
        await message.answer("Авторизация прошла успешно ✅")
        await show_main_menu(message, state)
    else:
        await message.answer("Неверный пароль. Попробуйте ещё раз 👇")

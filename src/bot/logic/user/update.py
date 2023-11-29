from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import joinedload, selectinload

from src.bot.fsm import MainGroup
from src.bot.fsm import ProfileMasterEditingGroup
from src.bot.fsm import ProfilePasswordEditingGroup
from src.bot.logic.user.get import show_user
from src.bot.logic.user.verify_id import id_verification_request
from src.bot.middlewares import TypingMd
from src.bot.utils.callback_manager import manager
from src.bot.utils.security import DataVerification
from src.bot.utils.security import Encryption
from src.db import Database
from src.db.models import AuthData
from src.db.models import Record
from src.db.models import User

router = Router()
router.message.middleware(TypingMd())


@router.callback_query(F.data == 'change_password', MainGroup.view_user)
async def type_old_password(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer('Получен запрос на смену пароля 🔑')
    await call.message.answer('Введите старый пароль ⬇️')
    await state.set_state(ProfilePasswordEditingGroup.typing_old_password)
    await call.answer()


@router.message(ProfilePasswordEditingGroup.typing_old_password)
async def type_new_password(message: types.Message, state: FSMContext, db: Database) -> None:
    await message.delete()

    async with db.session.begin():
        user = await db.user.get(message.from_user.id, options=[joinedload(User.auth_data)])

    if DataVerification.verify(message.text, user.auth_data.account_password, user.auth_data.salt):
        await message.answer('Пароль верный. Введите новый пароль ⬇️')
        await state.set_state(ProfilePasswordEditingGroup.typing_new_password)
    else:
        await message.answer('Неверный пароль. Введите старый пароль ⬇️')


@router.message(ProfilePasswordEditingGroup.typing_new_password)
async def update_password(message: types.Message, state: FSMContext, db: Database) -> None:
    await message.delete()

    async with db.session.begin():
        user = await db.user.get(message.from_user.id, options=[joinedload(User.auth_data)])
        auth_data: AuthData = user.auth_data
        auth_data.account_password = DataVerification.hash(message.text, auth_data.salt)
        await db.auth_data.merge(auth_data)

    await message.answer('Пароль успешно изменён ✅')
    await show_user(message, state, db)


@router.callback_query(F.data == 'change_master', MainGroup.view_user)
async def change_master_request(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer('Получен запрос на смену мастер-пароля 🔑')
    await id_verification_request(call.message, state, type_new_master, save_master=True)
    await call.answer()


@manager.callback
async def type_new_master(message: types.Message, state: FSMContext) -> None:
    await message.answer('Введите новый мастер-пароль ⬇️')
    await state.set_state(ProfileMasterEditingGroup.typing_new_password)


@router.message(ProfileMasterEditingGroup.typing_new_password, flags={'chat_action': 'typing'})
async def update_master(message: types.Message, state: FSMContext, db: Database) -> None:
    await message.delete()
    await message.answer('Подождите, это может занять какое-то время... ⏳')

    new_master = message.text
    user_data = await state.get_data()

    async with db.session.begin():
        user = await db.user.get(message.from_user.id, options=[
            joinedload(User.auth_data),
            selectinload(User.records)
        ])
        auth_data: AuthData = user.auth_data
        auth_data.master_password = DataVerification.hash(new_master, auth_data.salt)
        await db.auth_data.merge(auth_data)

        for record in user.records:
            record: Record
            old_salt = record.salt
            new_salt = Encryption.generate_salt()
            old_password = Encryption.decrypt(record.password_, user_data['master'], old_salt)
            new_password = Encryption.encrypt(old_password, new_master, new_salt)
            old_username = Encryption.decrypt(record.username, user_data['master'], old_salt)
            new_username = Encryption.encrypt(old_username, new_master, new_salt)

            record.salt = new_salt
            record.password_ = new_password
            record.username = new_username

            await db.record.merge(record)

    await message.answer('Мастер-пароль успешно изменён ✅')
    await show_user(message, state, db)
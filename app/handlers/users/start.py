from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.catalog import get_folder_keyboard


async def start_process_message(m: types.Message, db: AsyncSession):
    await m.answer(
        "Добро пожаловать в бота-хранилище!\n"
        "Тут вы можете создавать папки, хранить файлы и делиться ими с доверенными аккаунтами!",
        reply_markup=await get_folder_keyboard(db))


def register_start(dp: Dispatcher):
    dp.register_message_handler(start_process_message, CommandStart())

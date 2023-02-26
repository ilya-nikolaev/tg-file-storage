from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from app.callback_data.catalog import open_folder_cd, open_file_cd, add_new_folder_cd, add_new_file_cd
from app.db_api.funcs import get_folders_from_folder, get_files_from_folder
from app.db_api.models import Folder


async def get_folder_keyboard(db: AsyncSession, folder_id: int = None):
    folders = await get_folders_from_folder(db, folder_id)
    files = await get_files_from_folder(db, folder_id)

    back_part = []
    if folder_id:
        current_folder: Folder = await db.get(Folder, folder_id)
        back_part = [[InlineKeyboardButton(text="⬆️ Подняться на уровень выше",
                                           callback_data=open_folder_cd.new(folder_id=current_folder.parent_id or 0))]]

    controls_part = [
        [InlineKeyboardButton(text="➕📂 Добавить новую папку",
                              callback_data=add_new_folder_cd.new(parent_folder_id=folder_id or 0))],
        [InlineKeyboardButton(text="➕🗒 Добавить новый файл",
                              callback_data=add_new_file_cd.new(folder_id=folder_id or 0))]]

    folders_part = [[InlineKeyboardButton(text=f"📂 {folder.name}", callback_data=open_folder_cd.new(
        folder_id=folder.id))] for folder in folders]

    files_part = [[InlineKeyboardButton(text=f"🗒 {file.name}", callback_data=open_file_cd.new(
        file_id=file.id))] for file in files]

    return InlineKeyboardMarkup(inline_keyboard=back_part + controls_part + folders_part + files_part)

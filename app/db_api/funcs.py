from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_api.models import Folder, File


async def get_folders_from_folder(db: AsyncSession, folder_id: int = None) -> list[Folder]:
    query = select(Folder).where(Folder.parent_id == folder_id)
    return await db.scalars(query)


async def get_files_from_folder(db: AsyncSession, folder_id: int = None) -> list[File]:
    query = select(File).where(File.folder_id == folder_id)
    return await db.scalars(query)


async def get_folder_path(db: AsyncSession, folder_id: int = None) -> str:
    if not folder_id:
        return "\\"

    path = []

    folder = await db.get(Folder, folder_id)
    path.append(folder.name)

    while folder.parent_id:
        folder = await db.get(Folder, folder.parent_id)
        path.append(folder.name)

    return "\\" + "\\".join(reversed(path))


async def get_file_path(db: AsyncSession, file_id: int = None) -> str:
    file = await db.get(File, file_id)

    if not file.folder_id:
        return "\\" + file.name

    path = []

    folder = await db.get(Folder, file.folder_id)
    path.append(file.name)
    path.append(folder.name)

    while folder.parent_id:
        folder = await db.get(Folder, folder.parent_id)
        path.append(folder.name)

    return "\\" + "\\".join(reversed(path))

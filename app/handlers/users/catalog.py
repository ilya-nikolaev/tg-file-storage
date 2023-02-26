from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from sqlalchemy.ext.asyncio import AsyncSession

from app.callback_data.catalog import add_new_folder_cd, add_new_file_cd, open_folder_cd, open_file_cd
from app.db_api.funcs import get_folder_path, get_file_path
from app.db_api.models import Folder, File
from app.keyboards.catalog import get_folder_keyboard


async def add_new_folder(cq: types.CallbackQuery, state: FSMContext, callback_data: dict):
    parent_folder_id = int(callback_data['parent_folder_id'])
    await state.update_data({'parent_folder_id': parent_folder_id})

    await cq.answer()
    await cq.message.answer("Введите название папки")

    await state.set_state("waiting_for_folder_name")


async def process_folder_name(m: types.Message, db: AsyncSession, state: FSMContext):
    state_data = await state.get_data()
    parent_folder_id = state_data['parent_folder_id']
    folder_name = m.text

    if not parent_folder_id:
        parent_folder_id = None

    new_folder = Folder(parent_id=parent_folder_id, name=folder_name)
    db.add(new_folder)

    await db.commit()

    await m.answer(f"Новая папка с именем '{folder_name}' добавлена!",
                   reply_markup=await get_folder_keyboard(db, parent_folder_id))

    await state.reset_state()


async def add_new_file(cq: types.CallbackQuery, state: FSMContext, callback_data: dict):
    folder_id = int(callback_data['folder_id'])
    await state.update_data({'folder_id': folder_id})

    await cq.answer()
    await cq.message.answer("Отправьте файл для загрузки на сервер (имя файла будет видно всем)")

    await state.set_state("waiting_for_file")


async def process_file(m: types.Message, db: AsyncSession, state: FSMContext):
    state_data = await state.get_data()
    folder_id = state_data['folder_id']
    file = m.document

    if not folder_id:
        folder_id = None

    new_file = File(file_id=file.file_id, name=file.file_name, size=file.file_size,
                    folder_id=folder_id, owner=m.from_user.id)

    db.add(new_file)
    await db.commit()

    await m.answer(f"Файл '{file.file_name}' успешно загружен!",
                   reply_markup=await get_folder_keyboard(db, folder_id))

    await state.reset_state()


async def open_folder(cq: types.CallbackQuery, db: AsyncSession, callback_data: dict):
    await cq.answer()

    folder_id = int(callback_data['folder_id'])

    if not folder_id:
        folder_id = None

    await cq.message.edit_text(f"Путь: {await get_folder_path(db, folder_id)}",
                               reply_markup=await get_folder_keyboard(db, folder_id))


async def open_file(cq: types.CallbackQuery, db: AsyncSession, callback_data: dict):
    await cq.answer()

    file_id = int(callback_data['file_id'])
    file: File = await db.get(File, file_id)

    await cq.message.delete()
    await cq.message.answer_document(file.file_id, caption=f"Путь: {await get_file_path(db, file_id)}")
    await cq.message.answer(f"Путь: {await get_folder_path(db, file.folder_id)}",
                            reply_markup=await get_folder_keyboard(db, file.folder_id))


def register_catalog(dp: Dispatcher):
    dp.register_callback_query_handler(add_new_folder, add_new_folder_cd.filter())
    dp.register_message_handler(process_folder_name, state='waiting_for_folder_name')
    dp.register_callback_query_handler(add_new_file, add_new_file_cd.filter())
    dp.register_message_handler(process_file, state="waiting_for_file", content_types=[ContentType.DOCUMENT])
    dp.register_callback_query_handler(open_folder, open_folder_cd.filter())
    dp.register_callback_query_handler(open_file, open_file_cd.filter())

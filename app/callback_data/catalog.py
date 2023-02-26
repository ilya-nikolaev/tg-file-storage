from aiogram.utils.callback_data import CallbackData

open_folder_cd = CallbackData("open_folder", "folder_id")
open_file_cd = CallbackData("open_file", "file_id")

add_new_folder_cd = CallbackData("add_folder", "parent_folder_id")
add_new_file_cd = CallbackData("add_file", "folder_id")

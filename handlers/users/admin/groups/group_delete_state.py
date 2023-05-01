from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message

from loader import dp, db
from keyboards.inline.admin.group_delete_menu import generate_group_delete_menu
from keyboards.default.admin.admin_menu import generate_admin_main_menu


@dp.message_handler(Text("🗑 Удалить группу"))
async def group_delete_state_start(message: Message):
    await message.answer("<b>Выберите группу которую нужно удалить</b>",
                         reply_markup=generate_group_delete_menu())


@dp.callback_query_handler(lambda call: "group-delete" == call.data.split(":")[0])
async def group_delete(call: CallbackQuery):
    db.remove_from_groups_list(group_chat_id=int(call.data.split(":")[1]))
    await call.message.answer(f"<b>Группа успешно удалена ✔</b>",
                              reply_markup=generate_admin_main_menu())
    await call.message.delete()

from loader import dp
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.contrib.middlewares.fsm import FSMContext
from keyboards.default.admin import admin_menu
from keyboards.default import main_menu
from tools.permissions import is_admin


@dp.message_handler(Command("cancel"), state="*", )
@dp.message_handler(Text("❌ Отменить действия"), state="*")
async def cancel_any_state(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return None
    await state.finish()
    await message.answer("<b>Действия отменены ✅</b>",
                         reply_markup=admin_menu.generate_admin_main_menu() if is_admin(
                             message.from_user.id) else main_menu.generate_main_menu())

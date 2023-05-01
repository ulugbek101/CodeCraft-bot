from aiogram.dispatcher.filters import Text
from aiogram.contrib.middlewares.fsm import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from loader import dp, db
from states.admin.groups import GroupAddState
from keyboards.default.cancel_btn import generate_cancel_btn
from keyboards.default.admin.admin_menu import generate_admin_main_menu
from tools.permissions import is_admin, private_chat
from tools.weekdays_converter import convert_weekdays


@dp.message_handler(Text("🖋 Добавить группу"))
async def group_state_start(message: Message):
    if private_chat(message) and is_admin(message.from_user.id):
        await message.answer("<b>Введите ID группы, вы можете узнать её отправив команду /id в эту группу, "
                             "но сначала убедитесь, что бот добавлен в группу и является администратором</b>",
                             reply_markup=generate_cancel_btn())
        await GroupAddState.group_id.set()


@dp.message_handler(state=GroupAddState.group_id)
async def save_group_id(message: Message, state: FSMContext):
    await state.update_data(group_id=int(message.text))
    await GroupAddState.next()
    await message.answer("<b>Введите название группы, например: <i>Backend разработка на Python</i></b>",
                         reply_markup=generate_cancel_btn())


@dp.message_handler(state=GroupAddState.group_name)
async def save_group_name(message: Message, state: FSMContext):
    await state.update_data(group_name=message.text)
    await GroupAddState.next()
    await message.answer("<b>Введите дни занятий в числовом формате, например: 1,2,3\n"
                         "<i>1-Понедельник</i>\n"
                         "<i>2-Вторник</i>\n"
                         "<i>3-Среда</i>\n"
                         "<i>4-Четверг</i>\n"
                         "<i>5-Пятница</i>\n"
                         "<i>6-Суббота</i>\n"
                         "<i>7-Воскресенье</i>\n"
                         "1,3,5 --> Понедельник, Среда, Пятница</b>", reply_markup=generate_cancel_btn())


@dp.message_handler(state=GroupAddState.lesson_days)
async def save_lesson_days(message: Message, state: FSMContext):
    await state.update_data(lesson_days=message.text)
    await GroupAddState.next()
    await message.answer("<b>Введите время занятий, например: 14:00</b>", reply_markup=generate_cancel_btn())


@dp.message_handler(state=GroupAddState.lesson_time)
async def save_lesson_time(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['lesson_time'] = message.text
        lesson_days = ",".join(
            convert_weekdays([int(day) for day in data['lesson_days'].split(',') if day.strip().isdigit()]))
        msg = f"Название группы: <b><i>{data['group_name']}</i></b>\n" \
              f"ID группы: <code>{data['group_id']}</code>\n" \
              f"Дни занятий: <b><i>{lesson_days}</i></b>\n" \
              f"Время занятий: <b><i>{data['lesson_time']}</i></b>"
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да", callback_data="group-save:1"),
         InlineKeyboardButton(text="❌ Нет", callback_data="group-save:0")]
    ])
    await message.answer(f"{msg}\n\n<b>Все ли данные верны ?</b>", reply_markup=markup)
    await GroupAddState.next()


@dp.callback_query_handler(state=GroupAddState.confirmation)
async def save_or_not_group_info(call: CallbackQuery, state: FSMContext):
    if int(call.data.split(":")[1]) == 1:
        async with state.proxy() as data:
            group_id = data['group_id']
            group_name = data['group_name']
            lesson_days = data['lesson_days']
            lesson_time = data['lesson_time']
            try:
                db.register_group(group_id, group_name, lesson_days, lesson_time)
                await call.message.answer(f"<b>Группа <i>{data['group_name']}</i> добавлена !</b>",
                                          reply_markup=generate_admin_main_menu())
            except:
                await call.message.answer("<b>Группа с таким ID уже существует !</b>",
                                          reply_markup=generate_admin_main_menu())
        await state.finish()
        await call.message.delete()
    else:
        await state.finish()
        await call.message.answer("Действия отменены ✅", reply_markup=generate_admin_main_menu())
        await call.message.delete()

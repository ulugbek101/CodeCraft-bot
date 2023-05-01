from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.contrib.middlewares.fsm import FSMContext

from loader import dp, db
from tools import permissions
from states.admin.courses import CoursesState
from keyboards.default import cancel_btn, admin


@dp.message_handler(Text("🖋 Добавить курс"))
async def course_add_state_start(message: Message):
    if permissions.is_admin(message.from_user.id) and permissions.private_chat(message):
        await CoursesState.name.set()
        await message.answer("<b>Введите название курса</b>", reply_markup=cancel_btn.generate_cancel_btn())


@dp.message_handler(state=CoursesState.name)
async def save_course_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await CoursesState.next()
    await message.answer("<b>Отправьте краткое описание курса ( Краткий план обучения, что может сделать "
                         "студент академии по оканчанию курса, длительность и стоимость курса в конце )</b>",
                         reply_markup=cancel_btn.generate_cancel_btn())


@dp.message_handler(state=CoursesState.desc)
async def save_course_description(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
        name = data['name'].replace(' ', '_').lower()
        with open(file=f'media/courses-info/{name}.txt', mode='w', encoding='utf-8') as file:
            file.write(data['desc'])
    await CoursesState.next()
    await message.answer('<b>Отправьте фото ( логотип ) для курса c расширением "JPG"</b>',
                         reply_markup=cancel_btn.generate_cancel_btn())


@dp.message_handler(state=CoursesState.image_path, content_types='photo')
async def save_course_photo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        name = data['name'].replace(' ', '_').lower()
        data['image_path'] = f"media/courses-logo/{name}.jpg"
        await message.photo[-1].download(destination_file=f'media/courses-logo/{name}.jpg')
        try:
            db.register_course(data['name'], f'media/courses-info/{name}.txt', data['image_path'])
            await message.answer("<b>Курс успешно добавлен !</b>",
                                 reply_markup=admin.admin_menu.generate_admin_main_menu())
        except:
            await message.answer("<b>Курс с таким названием уже существует !</b>",
                                 reply_markup=admin.admin_menu.generate_admin_main_menu())
    await state.finish()

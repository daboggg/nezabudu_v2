from datetime import datetime, timedelta

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.formatting import as_list, Bold, as_key_value, Italic
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.main_ketboards import cancel_or_edit_kb
from bot.state_groups import Main
from bot.utils.converter import conv_voice
from bot.utils.from_datetime_to_str import datetime_to_str
from bot.utils.save_data import save_data
from parser_v2.parse import parse

main_handler = Router()


# дополнительно запрашиваем и сохраняем текст сообщения
@main_handler.message(Main.get_message)
async def get_message(message: Message, bot: Bot, state: FSMContext, apscheduler: AsyncIOScheduler, session: AsyncSession):
    state_data = await state.get_data()
    state_data.get("remind").get("messages")["message"] = message.text
    await set_remind(message, bot, state, apscheduler,session, message.from_user.id)


# сохраняем в бд, устанавливаем задание в скедулер
async def set_remind(message: Message, bot: Bot, state: FSMContext, apscheduler: AsyncIOScheduler, session: AsyncSession, user_id: int):
    state_data = await state.get_data()
    remind = state_data.get("remind")

    # todo убрать внизу принт
    print(remind)

    job = await save_data(state=state, bot=bot, session=session, apscheduler=apscheduler, user_id=user_id)
    item = []
    if rd:= remind.get("messages").get("period"):
        item.append(as_key_value("♾", Italic(rd)))
    remind_info =as_list(
        Bold("💡 Напоминание запланировано.\n"),
        as_key_value("⏰", Italic(datetime_to_str(job.next_run_time))),
        *item,
        as_key_value("📝", Italic(remind.get("messages").get("message"))),

    ).as_html()

    await state.clear()
    msg  = await message.answer(remind_info, reply_markup=cancel_or_edit_kb())

    # удалить клавиатуру через промежуток времени
    date = datetime.now() + timedelta(seconds=15)
    apscheduler.add_job(edit_msg, "date", run_date=date, kwargs={"message": msg})

# удаление клавиатуры
async def edit_msg(message: Message):
    await message.edit_reply_markup(reply_markup=None)


@main_handler.message(F.text | F.voice)
async def remind_me(message: Message, bot: Bot, state: FSMContext, apscheduler: AsyncIOScheduler, session: AsyncSession):
    try:
        remind = ''
        # если получили текст, отправляем в парсер
        if message.text:
            remind = parse(message.text)
        # если получили голосовое сообщение, конвертируем в текст и отправляем в парсер
        elif message.voice:
            text = await conv_voice(message=message, bot=bot)
            remind = parse(text)

        # если в напоминании присутствует текст сообщения, то отправляем на добавления задания
        if remind["messages"]["message"]:
            await state.update_data(remind=remind)
            await set_remind(message, bot, state, apscheduler, session, message.from_user.id)
        # если в напоминании отсутствует текст сообщения, дополнительно запрашиваем текст сообщения
        else:
            await state.update_data(remind=remind)
            await message.answer("введите текст напоминания")
            await state.set_state(Main.get_message)
    except Exception as e:
        # todo убрать внизу принт
        print(e)
        await message.answer("пожалуйста введите время и текст напоминания")


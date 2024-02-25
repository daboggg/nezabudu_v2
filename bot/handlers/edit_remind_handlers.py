from datetime import datetime, timedelta

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.formatting import Italic, as_key_value, as_list, Bold
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.keyboards.main_ketboards import cancel_or_edit_kb
from bot.state_groups import EditReminds
from bot.utils.converter import conv_voice
from bot.utils.from_datetime_to_str import datetime_to_str
from db.db_actions import edit_task_to_db
from parser_v2.parse import parse
from scheduler.scheduler_actions import edit_job_to_scheduler

edit_remind_handlers = Router()

# callback обрабатывает кнопу "исправить"
@edit_remind_handlers.callback_query(F.data.startswith("edit_remind"))
async def edit_start(callback: CallbackQuery, state: FSMContext, apscheduler: AsyncIOScheduler):
    await callback.answer()

    job_id = callback.data.split(":")[1]
    hide_kb_id = callback.data.split(":")[2]

    apscheduler.remove_job(hide_kb_id)

    job = apscheduler.get_job(job_id)
    msg = job.kwargs.get('text')
    await callback.message.edit_text(f"👉 {msg}")
    await callback.message.answer(Italic("введите время напоминания").as_html())
    await state.update_data(job_id=job_id)
    await state.set_state(EditReminds.get_remind_time)



# принимает для исправления текст или голосовое сообщение
@edit_remind_handlers.message(EditReminds.get_remind_time, F.text | F.voice)
async def get_remind_time(message: Message, bot: Bot, state: FSMContext, apscheduler: AsyncIOScheduler):

    try:
        remind = ''
        # если получили текст, отправляем в парсер
        if message.text:
            remind = parse(message.text)
        # если получили голосовое сообщение, конвертируем в текст и отправляем в парсер
        elif message.voice:
            text = await conv_voice(message=message, bot=bot)
            remind = parse(text)

        await state.update_data(params=remind.get("params"))
        await state.update_data(message=remind.get("messages").get("message"))
        await state.update_data(period=remind.get("messages").get("period"))

        await edit_remind(message, bot, state, apscheduler)

    except Exception:
        if message.text:
            await state.update_data(message=message.text)
        elif message.voice:
            text = await conv_voice(message=message, bot=bot)
            await state.update_data(message=text)

        await edit_remind(message, bot, state, apscheduler)


# редактирует напоминание
async def edit_remind(message: Message,
                      bot: Bot,
                      state: FSMContext,
                      apscheduler: AsyncIOScheduler,):
    job: Job = await edit_job_to_scheduler(apscheduler, bot, state)
    result = await edit_task_to_db(state, job)
    period = result[0]
    text = result[1]

    item = []
    if period:
        item.append(as_key_value("♾", Italic(period)))
    remind_info = as_list(
        Bold("💡 Напоминание запланировано.\n"),
        as_key_value("⏰", Italic(datetime_to_str(job.next_run_time))),
        *item,
        as_key_value("📝", Italic(text)),

    ).as_html()

    # очистить state
    await state.clear()

    # создать id для удаления клавиатуры
    hide_kb_id = f"{message.from_user.id}{datetime.now().second}"

    msg = await message.answer(remind_info, reply_markup=cancel_or_edit_kb(job.id, hide_kb_id))

    # удалить клавиатуру через промежуток времени
    date = datetime.now() + timedelta(seconds=15)
    apscheduler.add_job(edit_msg, "date", id=hide_kb_id, run_date=date, kwargs={"message": msg})

# удаление клавиатуры
async def edit_msg(message: Message):
    await message.edit_reply_markup(reply_markup=None)


# если пришел не текст и не голосовое сообщение
@edit_remind_handlers.message(EditReminds.get_remind_time)
async def request_remind_again(message: Message):
    await message.answer(Italic("введите время напоминания").as_html())

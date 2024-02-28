import time
from datetime import datetime, timedelta

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.formatting import as_list, Bold, as_key_value, Italic
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.keyboards.main_ketboards import cancel_or_edit_kb
from bot.state_groups import RescheduleReminds
from bot.utils.converter import conv_voice
from bot.utils.from_datetime_to_str import datetime_to_str
from bot.utils.save_data import save_data
from parser_v2.parse import parse

delay_remind_handlers = Router()


# отложить напоминание
@delay_remind_handlers.callback_query(F.data.startswith("delay_remind"))
async def delay_remind(callback: CallbackQuery, apscheduler: AsyncIOScheduler):
    tmp = callback.data.split(":")
    job_id = tmp[1]
    delay_time = int(tmp[2])
    job: Job = apscheduler.reschedule_job(job_id=job_id, trigger='date',
                                          run_date=datetime.now() + timedelta(minutes=delay_time))
    remind_info = as_list(
        Bold("💡 Напоминание отложено.\n"),
        as_key_value("⏰", Italic(datetime_to_str(job.next_run_time))),
        as_key_value("📝", Italic(job.kwargs.get("text"))),
    ).as_html()

    await callback.answer()
    await callback.message.edit_text(remind_info)


# напоминание выполнено
@delay_remind_handlers.callback_query(F.data.startswith("done_remind"))
async def delay_remind(callback: CallbackQuery, apscheduler: AsyncIOScheduler):
    tmp = callback.data.split(":")
    job_id = tmp[1]

    job: Job = apscheduler.get_job(job_id)

    format_text = as_list(
        Bold("\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──"),
        f"✔️ 👉{job.kwargs.get('text')}👈",
        Bold("\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──"),
    ).as_html()
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(format_text)
    job.remove()


# переназначить напоминание
@delay_remind_handlers.callback_query(F.data.startswith("reschedule_remind"))
async def reschedule_remind(callback: CallbackQuery, state: FSMContext, apscheduler: AsyncIOScheduler):
    tmp = callback.data.split(":")
    job_id = tmp[1]
    job = apscheduler.get_job(job_id)
    await state.update_data(job_id=job_id, user_id=int(job.name), text=job.kwargs.get("text"))
    job.remove()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()
    await callback.message.answer("введите время напоминания")
    await state.set_state(RescheduleReminds.get_remind)


@delay_remind_handlers.message(RescheduleReminds.get_remind, F.text | F.voice)
async def get_remind(message: Message, bot: Bot, state: FSMContext, apscheduler: AsyncIOScheduler):
    state_data = await state.get_data()
    remind = ''

    try:
    # если получили текст, отправляем в парсер
        if message.text:
            remind = parse(message.text)
        # если получили голосовое сообщение, конвертируем в текст и отправляем в парсер
        elif message.voice:
            text = await conv_voice(message=message, bot=bot)
            remind = parse(text)

        # если в напоминании присутствует текст сообщения, то отправляем на добавления задания
        if remind.get("messages").get("message"):
            await set_remind(message, remind, apscheduler, bot, state)
        # если в напоминании отсутствует текст сообщения, дополнительно запрашиваем текст сообщения
        else:
            text = state_data.get("text")
            remind["messages"]["message"] = text
            await set_remind(message, remind,  apscheduler, bot, state)

    except Exception as e:
        await message.answer('введите время напоминания')


# установить переназначенное напоминание
async def set_remind(message: Message,remind: dict, apscheduler: AsyncIOScheduler, bot: Bot, state: FSMContext):
    state_data = await state.get_data()
    user_id = state_data.get("user_id")
    await state.update_data(remind=remind)
    job = await save_data(state,bot,apscheduler, user_id)

    item = []
    if rd := remind.get("messages").get("period"):
        item.append(as_key_value("♾", Italic(rd)))
    remind_info = as_list(
        Bold("💡 Напоминание запланировано.\n"),
        as_key_value("⏰", Italic(datetime_to_str(job.next_run_time))),
        *item,
        as_key_value("📝", Italic(remind.get("messages").get("message"))),

    ).as_html()

    await state.clear()

    # создать id для удаления клавиатуры
    hide_kb_id = str(time.time_ns())

    msg = await message.answer(remind_info, reply_markup=cancel_or_edit_kb(job.id, hide_kb_id))

    # удалить клавиатуру через промежуток времени
    date = datetime.now() + timedelta(seconds=15)
    apscheduler.add_job(edit_msg, "date", id=hide_kb_id, run_date=date, kwargs={"message": msg})


# удаление клавиатуры
async def edit_msg(message: Message):
    await message.edit_reply_markup(reply_markup=None)


@delay_remind_handlers.message(RescheduleReminds.get_remind)
async def not_text_not_voice(message: Message):
    await message.answer("введите время напоминания")

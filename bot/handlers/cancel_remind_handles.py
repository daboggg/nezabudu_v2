from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.formatting import Strikethrough, Bold
from apscheduler.schedulers.asyncio import AsyncIOScheduler

cancel_remind_handlers = Router()

@cancel_remind_handlers.callback_query(F.data.startswith("cancel_remind"))
async def cancel_remind(callback: CallbackQuery, apscheduler: AsyncIOScheduler):
    await callback.answer()

    job_id = callback.data.split(":")[1]
    hide_kb_id = callback.data.split(":")[2]

    apscheduler.remove_job(hide_kb_id)
    apscheduler.remove_job(job_id)

    part_msg = callback.message.text.split("\n")
    msg = Bold(f"{part_msg[0].replace('запланировано','отменено')}\n").as_html() + Strikethrough('\n'.join(part_msg[1:])).as_html()

    await callback.message.edit_text(msg)




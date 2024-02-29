import json
import logging

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.handlers.send_remind_hendlers import send_reminder
from db.db_actions import get_tasks_from_db

logger = logging.getLogger(__name__)


# добавление задания в скедулер
async def add_job_to_scheduler(
        apscheduler: AsyncIOScheduler,
        bot: Bot,
        state: FSMContext,
        remind_id: int,
        user_id: int,
) -> Job:
    state_data = await state.get_data()
    remind = state_data.get("remind")
    params = remind.get("params")
    messages = remind.get("messages")

    job = apscheduler.add_job(
        send_reminder,
        **params,
        id=str(remind_id),
        name=str(user_id),
        kwargs={
            'apscheduler': apscheduler,
            'bot': bot,
            'chat_id': user_id,
            'text': messages.get('message'),
        }
    )
    return job


# изменение задания в скедулере
async def edit_job_to_scheduler(
        apscheduler: AsyncIOScheduler,
        bot: Bot,
        state: FSMContext,
):
    state_data = await state.get_data()

    params = state_data.get("params", None)
    message = state_data.get("message", None)
    job_id = state_data.get("job_id")
    job = apscheduler.get_job(job_id)

    if params and message:
        apscheduler.reschedule_job(
            job_id=str(job_id),
            **params
        )
        return apscheduler.modify_job(
            job_id=str(job_id),
            kwargs={
                'apscheduler': apscheduler,
                'bot': bot,
                'chat_id': int(job.name),
                'text': message,
            }
        )
    elif params:
        return apscheduler.reschedule_job(
            job_id=str(job_id),
            **params
        )
    else:
        return apscheduler.modify_job(
            job_id=str(job_id),
            kwargs={
                'apscheduler': apscheduler,
                'bot': bot,
                'chat_id': int(job.name),
                'text': message,
            }
        )


# восстановление заданий из базы данных
async def recovery_job_to_scheduler(apscheduler: AsyncIOScheduler, bot: Bot):
    if tasks := await get_tasks_from_db():
        for task in tasks:
            tmp = json.loads(task.params)

            apscheduler.add_job(
                send_reminder,
                **tmp,
                id=str(task.id),
                name=str(task.chat_id),
                kwargs={
                    'apscheduler': apscheduler,
                    'bot': bot,
                    'chat_id': task.chat_id,
                    'text': task.text,
                }
            )

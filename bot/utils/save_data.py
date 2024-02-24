from aiogram import Bot
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db.db_actions import add_remind_to_db
from scheduler.scheduler_actions import add_job_to_scheduler


async def save_data(state: FSMContext, bot: Bot, apscheduler: AsyncIOScheduler, user_id: int):
    # сохранить в бд задание
    remind_id = await add_remind_to_db(state, user_id)
    # установить задание в скедулер и вернуть его
    return await add_job_to_scheduler(apscheduler, bot, state, remind_id, user_id)

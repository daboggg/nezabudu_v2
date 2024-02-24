import json
import logging

import apscheduler.events
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_helper import db_helper
from models import Remind

logger = logging.getLogger(__name__)


# добавить задание в бд
async def add_remind_to_db(state: FSMContext, user_id: int) -> int:
    session = db_helper.get_scoped_session()
    state_data = await state.get_data()
    remind = state_data.get("remind")
    params = remind.get("params")
    messages = remind.get("messages")

    # если run_date присутствует в словаре, преобразуем datetime в строку
    if rd := params.get("run_date"):
        params["run_date"] = str(rd)

    remind = Remind(
        params=json.dumps(params),
        chat_id=user_id,
        text=messages.get('message'),
        period=messages.get('period', None),
    )
    print(session)
    session.add(remind)
    await session.flush()
    remind_id = remind.id
    await session.commit()
    await session.close()

    return remind_id


# взять все задания из бд
async def get_tasks_from_db() -> list[Remind]:
    session = db_helper.get_scoped_session()

    result: Result = await session.execute(select(Remind))
    tasks = result.scalars().all()
    await session.close()

    return list(tasks)


# удалить задание из бд
async def delete_task_from_db(job: apscheduler.events.JobEvent):
    session: AsyncSession = db_helper.get_scoped_session()
    result = await session.execute(select(Remind).where(Remind.id == int(job.job_id)))
    if task := result.scalar():
        logger.info(f"удален job с id: {job.job_id}")
        await session.delete(task)
    await session.commit()
    await session.close()

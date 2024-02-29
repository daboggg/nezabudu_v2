import json
import operator
from datetime import datetime
from typing import Any

from aiogram.types import CallbackQuery
from aiogram.utils.formatting import as_key_value, Italic, as_list, Bold
from aiogram_dialog import Dialog, Window, DialogManager, Data
from aiogram_dialog.widgets.kbd import Select, Column, Button, Back, ScrollingGroup
from aiogram_dialog.widgets.text import Const, Format, Case
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.state_groups import ListOfReminders
from bot.utils.from_datetime_to_str import datetime_to_short_str, datetime_to_str
from db.db_actions import get_tasks_from_db, get_task_from_db, get_tasks_from_db_by_user_id
from models import Remind


async def get_reminders(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.event.from_user.id
    result = list()
    reminders = await get_tasks_from_db_by_user_id(user_id)
    for reminder in reminders:
        datetime_str = None
        text = reminder.text
        if reminder.period:
            datetime_str = reminder.period
        else:
            params: dict = json.loads(reminder.params)
            run_date = params.get("run_date")
            dt = datetime.fromisoformat(run_date)
            datetime_str = datetime_to_short_str(dt)
        result.append((datetime_str, text, reminder.id))

    return {
        "reminders": result,
        "count": str(len(reminders)),
    }


async def get_reminder(dialog_manager: DialogManager, **kwargs):
    reminder_id = dialog_manager.dialog_data.get("reminder_id")
    apscheduler: AsyncIOScheduler = dialog_manager.middleware_data.get("apscheduler")

    job = apscheduler.get_job(reminder_id)
    reminder: Remind = await get_task_from_db(int(reminder_id))

    item = []
    if rd := reminder.period:
        item.append(as_key_value("♾", Italic(rd)))
    remind_info = as_list(
        as_key_value("⏰", Italic(datetime_to_str(job.next_run_time))),
        *item,
        as_key_value("📝", Italic(reminder.text)),

    ).as_html()

    return {"remind_info": remind_info}

async def on_reminder_selected(callback: CallbackQuery, widget: Any,
                               manager: DialogManager, reminder_id: str):
    manager.dialog_data["reminder_id"] = reminder_id
    await manager.switch_to(ListOfReminders.show_reminder)


async def on_delete_selected(callback: CallbackQuery, button: Button,
                     dialog_manager: DialogManager):
    apscheduler: AsyncIOScheduler = dialog_manager.middleware_data.get("apscheduler")
    apscheduler.remove_job(dialog_manager.dialog_data.get("reminder_id"))
    await callback.answer("напоминание удалено")
    del dialog_manager.dialog_data["reminder_id"]
    await dialog_manager.switch_to(ListOfReminders.start)


# диалог список напоминаний
list_reminders_dialog = Dialog(
    Window(
        Const("📄 Список напоминаний:"),
        Case(
            {
                "0": Const("            🫲   🫱"),
                ...: Format("           всего: {count} 👇")
            },
            selector="count"
        ),
        ScrollingGroup(
            Select(
                Format("{item[0]} {item[1]}"),
                id="s_reminders",
                item_id_getter=operator.itemgetter(2),
                items="reminders",
                on_click=on_reminder_selected,
            ),
            id='scroll',
            width=1,
            height=7
        ),
        state=ListOfReminders.start,
        getter=get_reminders,
    ),
    Window(
        Format('{remind_info}'),
        Back(Const("Назад")),
        Button(Const("Удалить"),id='delete_reminder', on_click=on_delete_selected),
        state=ListOfReminders.show_reminder,
        getter=get_reminder,
    ),
)

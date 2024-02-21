import asyncio

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.utils.formatting import as_list, Bold, Italic, as_marked_section, as_key_value
from aiogram_dialog import Dialog, Window, DialogManager, BaseDialogManager
from aiogram_dialog.manager.bg_manager import BgManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row, Start, Button
from aiogram_dialog.widgets.text import Const, Format
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.dialogs.state_groups import MainSG


async def background(manager: BaseDialogManager):
    await asyncio.sleep(6)
    await manager.update({
        "two": False,
        "text": "lklklk"
    })
    print("lklklk")
    # await asyncio.sleep(1)
    # await manager.done()


async def window1_get_data(dialog_manager: DialogManager, **kwargs):
    # bg: BgManager = dialog_manager.

    # try:
    #     if text := dialog_manager.event.text:
    #         job = get_job_from_text(text)
    #     elif text := dialog_manager.event.voice:
    #         pass
    # except:
    #     pass
    # text: str = 'no'
    # if dialog_manager.event.text == 'da':
    #     text = 'da'
    # asyncio.get_running_loop().create_task(delay(dialog_manager))

    return {
        "two": dialog_manager.dialog_data.get("two", True),
        "text": dialog_manager.dialog_data.get("text", "asad")
    }


# главный диалог
main_dialog = Dialog(
    Window(
        Const('asad'),
        Format("asa : {text}"),
        # Format("asa : {dialog_data[one]}"),
        # TextInput(id="criterion", on_success=next_state_or_finish_state),
        # Row(
        #     Start(Const("список напоминаний"), id="list_tasks", state=ListOfRemindersSG.start,
        #           on_click=list_tasks_clicked),
        #     Start(Const("помощь"), id="help", state=HelpSG.start),
        # ),
        Button(Const("принять"), id="accept", when=F["two"]),
        state=MainSG.start,
        getter=window1_get_data,
    ),
    Window(
        Const('wertt'),
        # Format("asa : {dialog_data[one]}"),
        # TextInput(id="criterion", on_success=next_state_or_finish_state),
        # Row(
        #     Start(Const("список напоминаний"), id="list_tasks", state=ListOfRemindersSG.start,
        #           on_click=list_tasks_clicked),
        #     Start(Const("помощь"), id="help", state=HelpSG.start),
        # ),
        state=MainSG.second,
    ),
)


async def delay(dialog_manager: DialogManager, ):
    # suspend for a time limit in seconds
    await asyncio.sleep(6)
    # execute the other coroutine
    # await dialog_manager.update({"one": "two"})
    await dialog_manager.bg().next()

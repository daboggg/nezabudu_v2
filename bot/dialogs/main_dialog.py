# import asyncio
# from time import time, sleep
# from typing import Any
#
# from aiogram import F
# from aiogram.types import CallbackQuery
# from aiogram.utils.formatting import as_list, Bold, Italic, as_marked_section, as_key_value
# from aiogram_dialog import Dialog, Window, DialogManager, BaseDialogManager, Data
# from aiogram_dialog.manager.bg_manager import BgManager
# from aiogram_dialog.widgets.input import TextInput
# from aiogram_dialog.widgets.kbd import Row, Start, Button, Cancel
# from aiogram_dialog.widgets.text import Const, Format
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
#
# from bot.dialogs.state_groups import MainSG, SubDialog
# from bot.utils.save_data import save_data
#
#
# async def window1_get_data(dialog_manager: DialogManager, **kwargs):
#     # job = await save_data(dialog_manager)
#     # print(job.next_run_time)
#
#     # messages = dialog_manager.start_data.get("messages")
#     # params = dialog_manager.start_data.get("params")
#     # dialog_manager.start_data["messages"]["message"] = "test"
#     # print(params)
#     # print(messages)
#     print("OOOOOOOOOOOOOOOOOOO")
#     return {
#         # "time": str(job.next_run_time),
#         # "text": dialog_manager.start_data.get('messages').get('message')
#         "text": 'jjjjuuuyyy'
#     }
#
#
# async def main_process_result(start_data: Data, result: Any,
#                               dialog_manager: DialogManager):
#     print("We have result:", result)
#
#
# async def set_text_and_switch_to_ready_state(event, widget, dialog_manager: DialogManager, *_):
#     dialog_manager.start_data.get("messages")["message"] = dialog_manager.find('text').get_value()
#     # await dialog_manager.switch_to(MainSG.ready)
#     print("fffffffffffffffffff")
#     # asyncio.create_task(background(dialog_manager.bg()))
#
#
# remind_info = Format(
#     as_list(
#         Bold("💡 Напоминание запланировано.\n"),
#         as_key_value("⏰", Italic("{time}")),
#         as_key_value("📝", Italic("{text}")),
#     ).as_html()),
#
# # главный диалог
# main_dialog = Dialog(
#     Window(
#         # *remind_info,
#         Const('asad'),
#         # TextInput(id="text"),
#         Format("asa : {text}"),
#         # Format("asa : {dialog_data[one]}"),
#         # TextInput(id="criterion", on_success=next_state_or_finish_state),
#         # Row(
#         #     Start(Const("список напоминаний"), id="list_tasks", state=ListOfRemindersSG.start,
#         #           on_click=list_tasks_clicked),
#         #     Start(Const("помощь"), id="help", state=HelpSG.start),
#         # ),
#         # Button(Const("принять"), id="accept", when=F["two"]),
#         Cancel(),
#         state=MainSG.ready,
#         getter=window1_get_data,
#     ),
#     Window(
#         Const('введите текст напоминания'),
#         TextInput(id="text", on_success=set_text_and_switch_to_ready_state),
#         # Format("asa : {dialog_data[one]}"),
#         # TextInput(id="criterion", on_success=next_state_or_finish_state),
#         # Row(
#         #     Start(Const("список напоминаний"), id="list_tasks", state=ListOfRemindersSG.start,
#         #           on_click=list_tasks_clicked),
#         #     Start(Const("помощь"), id="help", state=HelpSG.start),
#         # ),
#         state=MainSG.not_ready,
#     ),
#     on_process_result=main_process_result,
# )
#
#
# async def close_subdialog(callback: CallbackQuery, button: Button,
#                           manager: DialogManager):
#     await manager.done(result={"name": "Tishka17"})
#
#
# second_dialog = Dialog(
#     Window(
#         Const("Subdialog"),
#         Button(Const("Close"), id="btn", on_click=close_subdialog),
#         Cancel(Const("Close")),
#         state=SubDialog.start,
#     )
# )
#
#
# async def delay(dialog_manager: DialogManager, ):
#     # suspend for a time limit in seconds
#     await asyncio.sleep(6)
#     # execute the other coroutine
#     # await dialog_manager.update({"one": "two"})
#     await dialog_manager.bg().next()

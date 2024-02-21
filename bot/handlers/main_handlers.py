import asyncio

from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.utils.formatting import as_list
from aiogram_dialog import DialogManager, StartMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.converter import conv_voice
from bot.dialogs.main_dialog import background
from bot.dialogs.state_groups import MainSG
from parser_v2.parse import parse

main_handler = Router()


@main_handler.message(F.text | F.voice)
async def remind_me(message: Message, bot: Bot, dialog_manager: DialogManager):
    try:
        remind = ''
        if message.text:
            remind = parse(message.text)
            print(remind)

        elif message.voice:
            text = await conv_voice(message=message, bot=bot)
            remind = parse(text)
            print(remind)
            # await dialog_manager.start(MainSG.start, mode=StartMode.RESET_STACK, data={"one": "one"})
            # print(remind)
        await message.answer(str(remind))
    except:
        await message.answer("пожалуйста введите время и текст напоминания")
    # print("tut")
    # if message.text:
    #     await message.answer("text")
    #     print("da")
    # if message.voice:
    #     await message.answer("voice")
    #     print("no")

    # await dialog_manager.start(MainSG.start, mode=StartMode.RESET_STACK, data={"one":"one"})
    # asyncio.create_task(background(dialog_manager.bg()))

    # result = parse(message.text)
    # print(result)
    # job = apscheduler.add_job(
    #     send_reminder,
    #     **result["params"],
    #     kwargs={
    #         'bot': bot,
    #         'chat_id': message.from_user.id,
    #         'text': result["messages"]["message"],
    #     }
    # )
    # await message.answer()


# функция для отправки напоминаний
async def send_reminder(bot: Bot, chat_id: int, text: str) -> None:
    # форматирование текста для напоминания
    format_text = as_list(
        "\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──",
        f"👉{text}👈",
        "\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──",
    )
    await bot.send_message(chat_id, format_text.as_html(), parse_mode='HTML')

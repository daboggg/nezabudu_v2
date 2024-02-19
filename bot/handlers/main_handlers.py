from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.utils.formatting import as_list
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from parser_v2.parse import parse

main_handler = Router()


@main_handler.message()
async def remind_me(message: Message, bot: Bot, apscheduler: AsyncIOScheduler):
    result = parse(message.text)
    print(result)
    job = apscheduler.add_job(
        send_reminder,
        **result["params"],
        kwargs={
            'bot': bot,
            'chat_id': message.from_user.id,
            'text': result["messages"]["message"],
        }
    )
    print(type(job.next_run_time))
    await message.answer(str(job.next_run_time))


# функция для отправки напоминаний
async def send_reminder(bot: Bot, chat_id: int, text: str) -> None:
    # форматирование текста для напоминания
    format_text = as_list(
        "\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──",
        f"👉{text}👈",
        "\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──",
    )
    await bot.send_message(chat_id, format_text.as_html(), parse_mode='HTML')

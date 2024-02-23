from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.formatting import as_list

cmd_router = Router()


# @cmd_router.message(CommandStart())
# async def cmd_start(_, dialog_manager: DialogManager) -> None:
#     pass


# @cmd_router.message(Command(commands="help"))
# async def cmd_start(message: Message) -> None:
#     await message.answer("помощь помощь")


# @cmd_router.message(Command(commands="list_of_reminds"))
# async def cmd_start(_, dialog_manager: DialogManager) -> None:
#     await dialog_manager.start(ListOfRemindersSG.start, mode=StartMode.RESET_STACK)
#




# функция для отправки напоминаний
async def send_reminder(bot: Bot, chat_id: int, text: str) -> None:
    # форматирование текста для напоминания
    format_text = as_list(
        "\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──",
        f"👉{text}👈",
        "\t── ⋆⋅☆⋅⋆ ── ⋆⋅☆⋅⋆ ──",
    )
    await bot.send_message(chat_id, format_text.as_html(), parse_mode='HTML')

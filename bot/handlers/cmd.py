from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.formatting import Bold, as_marked_section, as_list
from aiogram_dialog import DialogManager, StartMode

from bot.state_groups import ListOfReminders

cmd_router = Router()


@cmd_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("пожалуйста введите время и текст напоминания ")


@cmd_router.message(Command(commands="help"))
async def cmd_start(message: Message) -> None:
    title = Bold("📌 Используйте примеры для установки напоминания.\n")
    examples = as_marked_section(
        Bold("Например:"),
        "через 20 минут",
        "через 1 месяц, 2 дня, 6 часов",
        "через 1 год 20 минут",
        "в среду в 18.00",
        "в пятницу"
        "в 13:30",
        "завтра в 23-36",
        "послезавтра в 23-36",
        "31 декабря в 22.17",
        "12.12.24 в 8.55",
        "каждый день 19-30",
        "каждую субботу в 13:14",
        "каждое 17 апреля",
        "каждое 14 число",
        "каждое 14 число в 12:12",
        marker="✔️ "
    )
    help_text = as_list(title, examples)


    await message.answer(help_text.as_html())


@cmd_router.message(Command(commands="list"))
async def cmd_start(_, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(ListOfReminders.start, mode=StartMode.RESET_STACK)


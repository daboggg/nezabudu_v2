from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from bot.state_groups import ListOfReminders

cmd_router = Router()


@cmd_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("пожалуйста введите время и текст напоминания ")


# @cmd_router.message(Command(commands="help"))
# async def cmd_start(message: Message) -> None:
#     await message.answer("помощь помощь")


@cmd_router.message(Command(commands="list"))
async def cmd_start(_, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(ListOfReminders.start, mode=StartMode.RESET_STACK)


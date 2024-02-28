from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

cmd_router = Router()


@cmd_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("пожалуйста введите время и текст напоминания ")


# @cmd_router.message(Command(commands="help"))
# async def cmd_start(message: Message) -> None:
#     await message.answer("помощь помощь")


# @cmd_router.message(Command(commands="list_of_reminds"))
# async def cmd_start(_, dialog_manager: DialogManager) -> None:
#     await dialog_manager.start(ListOfRemindersSG.start, mode=StartMode.RESET_STACK)
#

from aiogram.fsm.state import StatesGroup, State


class Main(StatesGroup):
    get_message = State()

class EditReminds(StatesGroup):
    get_remind_time = State()

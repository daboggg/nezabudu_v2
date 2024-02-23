from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def cancel_or_edit_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()

    ikb.button(text=f'Отмена', callback_data=f'cancel')
    ikb.button(text=f'Изменить', callback_data=f'edit')

    return ikb.adjust(1).as_markup()
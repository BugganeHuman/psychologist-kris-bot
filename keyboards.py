from aiogram import types
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_request_type_panel():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="❤️ Здоровье", callback_data="request_type_health")
    )
    builder.row(
        InlineKeyboardButton(
            text="🫶 Отношения", callback_data="request_type_relationship"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="💰 Бизнесс / Финансы", callback_data="request_type_finance"
        )
    )
    return builder.as_markup()

def get_result_panel():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text='Получить результат ✅', callback_data=f'get_result')
    )
    return builder.as_markup()
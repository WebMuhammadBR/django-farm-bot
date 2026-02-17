from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Фермерлар рўйхати")],
        [KeyboardButton(text="📑 Шартномалар")],
        [KeyboardButton(text="🌾 Минерал ўғит")],
    ],
    resize_keyboard=True
)


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def farmers_pagination_keyboard(page: int, has_next: bool):

    buttons = []
    row = []

    if page > 1:
        row.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"farmers_page:{page-1}"
            )
        )

    row.append(
        InlineKeyboardButton(
            text="📥 Excel",
            callback_data="farmers_export_excel"
        )
    )

    if has_next:
        row.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"farmers_page:{page+1}"
            )
        )

    buttons.append(row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)




def contracts_pagination_keyboard(page: int, has_next: bool):

    buttons = []
    row = []

    if page > 1:
        row.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"contracts_page:{page-1}"
            )
        )

    row.append(
        InlineKeyboardButton(
            text="📥 Excel",
            callback_data="contracts_export_excel"
        )
    )

    if has_next:
        row.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"contracts_page:{page+1}"
            )
        )

    buttons.append(row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)




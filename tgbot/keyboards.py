from urllib.parse import quote

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Фермерлар")],
        [KeyboardButton(text="📑 Шартномалар")],
        [KeyboardButton(text="🌾 Минерал ўғит")],
    ],
    resize_keyboard=True
)


farmers_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Фермерлар рўйхати")],
        [KeyboardButton(text="🏠 Асосий меню")],
    ],
    resize_keyboard=True,
)

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




def contracts_filter_keyboard(districts: list[str]):
    buttons = [[InlineKeyboardButton(text="📊 Умумий", callback_data="contracts_filter:all:1")]]

    for district in districts:
        district_encoded = quote(district, safe="")
        buttons.append(
            [InlineKeyboardButton(text=district, callback_data=f"contracts_filter:{district_encoded}:1")]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def contracts_pagination_keyboard(page: int, has_next: bool, district: str):
    district_encoded = quote(district, safe="")

    buttons = []
    row = []

    if page > 1:
        row.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"contracts_filter:{district_encoded}:{page-1}"
            )
        )

    row.append(
        InlineKeyboardButton(
            text="📥 Excel",
            callback_data=f"contracts_export_excel:{district_encoded}"
        )
    )

    if has_next:
        row.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"contracts_filter:{district_encoded}:{page+1}"
            )
        )

    buttons.append(row)
    buttons.append(
        [InlineKeyboardButton(text="⬅️ Туманлар рўйхати", callback_data="contracts_back_to_filters")]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


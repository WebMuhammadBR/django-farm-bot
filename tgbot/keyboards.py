from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Фермерлар рўйхати")],
        [KeyboardButton(text="📑 Шартномалар")],
        [KeyboardButton(text="🌾 Минерал ўғит")],
    ],
    resize_keyboard=True,
)


def farmers_pagination_keyboard(page: int, has_next: bool):
    row = []

    if page > 1:
        row.append(InlineKeyboardButton(text="⬅️", callback_data=f"farmers_page:{page - 1}"))

    row.append(InlineKeyboardButton(text="📥 Excel", callback_data="farmers_export_excel"))

    if has_next:
        row.append(InlineKeyboardButton(text="➡️", callback_data=f"farmers_page:{page + 1}"))

    return InlineKeyboardMarkup(
        inline_keyboard=[
            row,
            [InlineKeyboardButton(text="🏠 Асосий меню", callback_data="menu:main")],
        ]
    )


def contracts_filters_keyboard(districts: list[str]):
    rows = [[InlineKeyboardButton(text="📊 Умумий", callback_data="contracts_filter:all")]]

    for index, district_name in enumerate(districts):
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"📍 {district_name}",
                    callback_data=f"contracts_filter:district:{index}",
                )
            ]
        )

    rows.append([InlineKeyboardButton(text="🏠 Асосий меню", callback_data="menu:main")])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def contracts_pagination_keyboard(page: int, has_next: bool, filter_token: str):
    row = []

    if page > 1:
        row.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"contracts_page:{page - 1}:{filter_token}",
            )
        )

    row.append(
        InlineKeyboardButton(
            text="📥 Excel",
            callback_data=f"contracts_export_excel:{filter_token}",
        )
    )

    if has_next:
        row.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"contracts_page:{page + 1}:{filter_token}",
            )
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            row,
            [InlineKeyboardButton(text="🔙 Туманлар", callback_data="contracts_back:filters")],
            [InlineKeyboardButton(text="🏠 Асосий меню", callback_data="menu:main")],
        ]
    )

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Фермерлар")],
        [KeyboardButton(text="📑 Шартномалар")],
        [KeyboardButton(text="🏬 Омбор")],
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


mineral_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌾 Минерал ўғит омбори")],
        [KeyboardButton(text="🏠 Асосий меню")],
    ],
    resize_keyboard=True,
)


warehouse_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📊 Ҳисобот"),
            KeyboardButton(text="📥 Кирим"),
            KeyboardButton(text="📤 Чиқим"),
        ],
        [KeyboardButton(text="🏬 Омбор")],
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
    buttons = [[InlineKeyboardButton(text="📊 Умумий", callback_data="contracts_filter:0:1")]]

    for index, district in enumerate(districts, start=1):
        buttons.append(
            [InlineKeyboardButton(text=district, callback_data=f"contracts_filter:{index}:1")]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def contracts_pagination_keyboard(page: int, has_next: bool, district_index: int):

    buttons = []
    row = []

    if page > 1:
        row.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"contracts_filter:{district_index}:{page-1}"
            )
        )

    row.append(
        InlineKeyboardButton(
            text="📥 Excel",
            callback_data=f"contracts_export_excel:{district_index}"
        )
    )

    if has_next:
        row.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"contracts_filter:{district_index}:{page+1}"
            )
        )

    buttons.append(row)
    buttons.append(
        [InlineKeyboardButton(text="⬅️ Туманлар рўйхати", callback_data="contracts_back_to_filters")]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)

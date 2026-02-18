from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Фермерлар")],
        [KeyboardButton(text="🏬 Омбор")],
    ],
    resize_keyboard=True
)


farmers_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Фермер Баланс")],
        [KeyboardButton(text="📑 Шартномалар")],
        [KeyboardButton(text="🏠 Асосий меню")],
    ],
    resize_keyboard=True,
)


warehouse_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📥 Кирим"),
            KeyboardButton(text="📤 Чиқим"),
        ],
        [KeyboardButton(text="🏠 Асосий меню")],
    ],
    resize_keyboard=True,
)


def warehouse_names_menu(warehouse_names: list[str]):
    rows = [[KeyboardButton(text=name)] for name in warehouse_names if name]
    rows.append([KeyboardButton(text="🏠 Асосий меню")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)




def farmers_filter_keyboard(districts: list[str]):
    buttons = [[InlineKeyboardButton(text="📊 Умумий", callback_data="farmers_filter:0:1")]]

    for index, district in enumerate(districts, start=1):
        buttons.append(
            [InlineKeyboardButton(text=district, callback_data=f"farmers_filter:{index}:1")]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def farmers_pagination_keyboard(page: int, has_next: bool, district_index: int):

    buttons = []
    row = []

    if page > 1:
        row.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"farmers_filter:{district_index}:{page-1}"
            )
        )

    row.append(
        InlineKeyboardButton(
            text="📥 Excel",
            callback_data=f"farmers_export_excel:{district_index}"
        )
    )

    if has_next:
        row.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"farmers_filter:{district_index}:{page+1}"
            )
        )

    buttons.append(row)
    buttons.append(
        [InlineKeyboardButton(text="⬅️ Туманлар рўйхати", callback_data="farmers_back_to_filters")]
    )

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


def warehouse_sections_inline_keyboard(warehouse_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📥 Кирим", callback_data=f"warehouse_section:{warehouse_id}:receipt")],
            [InlineKeyboardButton(text="📤 Чиқим", callback_data=f"warehouse_section:{warehouse_id}:expense")],
        ]
    )


def warehouse_expense_districts_inline_keyboard(warehouse_id: int, districts: list[dict]):
    buttons = [
        [
            InlineKeyboardButton(
                text="📊 Умумий",
                callback_data=f"warehouse_expense_district:{warehouse_id}:0",
            )
        ]
    ]

    for item in districts:
        district_id = item.get("district_id")
        district_name = item.get("district_name")
        if not district_id or not district_name:
            continue

        buttons.append(
            [
                InlineKeyboardButton(
                    text=str(district_name),
                    callback_data=f"warehouse_expense_district:{warehouse_id}:{district_id}",
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def warehouse_products_inline_keyboard(warehouse_id: int, movement: str, products: list[dict]):
    buttons = []
    for item in products:
        product_id = item.get("product_id")
        product_name = item.get("product_name")
        if not product_id or not product_name:
            continue

        buttons.append(
            [
                InlineKeyboardButton(
                    text=str(product_name),
                    callback_data=f"warehouse_product:{warehouse_id}:{movement}:{product_id}"
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="📥 Excel",
                callback_data=f"warehouse_export:{warehouse_id}:{movement}"
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)

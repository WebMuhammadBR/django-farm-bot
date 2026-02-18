from aiogram import F, Router
from aiogram.types import BufferedInputFile, CallbackQuery, Message

from tgbot.excel_export import warehouse_expenses_to_excel, warehouse_receipts_to_excel
from tgbot.keyboards import (
    warehouse_expense_districts_inline_keyboard,
    warehouse_menu,
    warehouse_names_menu,
    warehouse_products_inline_keyboard,
    warehouse_sections_inline_keyboard,
)
from tgbot.middlewares.access import access_required
from tgbot.services.api_client import (
    get_warehouse_expenses,
    get_warehouse_expense_districts,
    get_warehouse_movements,
    get_warehouse_products,
    get_warehouse_receipts,
    get_warehouse_totals_by_filters,
    get_warehouses,
)

router = Router()

WAREHOUSE_RECEIPT_NAMES = {"📥 Кирим", "kirim", "krim", "кирим"}
WAREHOUSE_EXPENSE_NAMES = {"📤 Чиқим", "chiqim", "чиқим"}


async def _warehouse_map():
    warehouses = await get_warehouses()
    return {
        int(item["id"]): str(item.get("name", "")).strip()
        for item in warehouses
        if item.get("id") and str(item.get("name", "")).strip()
    }


@router.message(F.text.in_({"🌾 Минерал ўғит", "🏬 Омбор"}))
@access_required
async def mineral_menu_handler(message: Message):
    warehouse_map = await _warehouse_map()
    if not warehouse_map:
        await message.answer(
            "Омборлар топилмади. Қуйидаги тугмалардан фойдаланинг 👇",
            reply_markup=warehouse_menu,
        )
        return

    await message.answer(
        "🏬 Омборлар рўйхати 👇",
        reply_markup=warehouse_names_menu(list(warehouse_map.values())),
    )


@router.message(F.text.func(lambda value: value and value.lower() in {name.lower() for name in WAREHOUSE_RECEIPT_NAMES}))
@access_required
async def warehouse_receipts_handler(message: Message):
    receipts = await get_warehouse_receipts()

    if not receipts:
        await message.answer("Кирим рўйхати бўш", reply_markup=warehouse_menu)
        return

    lines = ["📥 Омбор кирим рўйхати", ""]
    for index, item in enumerate(receipts[:30], start=1):
        invoice_number = item.get("invoice_number") or "-"
        bag_count = item.get("bag_count") or 0
        quantity = float(item.get("quantity") or 0)
        date = item.get("date") or "-"

        lines.append(
            f"{index}. {date} | №{invoice_number}\n"
            f"   Қоп: {bag_count} | Миқдор: {quantity:.2f}"
        )

    text = "\n".join(lines)
    await message.answer(f"<pre>{text}</pre>", parse_mode="HTML", reply_markup=warehouse_menu)


@router.message(F.text.func(lambda value: value and value.lower() in {name.lower() for name in WAREHOUSE_EXPENSE_NAMES}))
@access_required
async def warehouse_expenses_handler(message: Message):
    expenses = await get_warehouse_expenses()

    if not expenses:
        await message.answer("Чиқим рўйхати бўш", reply_markup=warehouse_menu)
        return

    lines = ["📤 Омбор чиқим рўйхати", ""]
    for index, item in enumerate(expenses[:30], start=1):
        date = item.get("date") or "-"
        farmer_name = item.get("farmer_name") or "-"
        quantity = float(item.get("quantity") or 0)
        number = item.get("number") or "-"
        lines.append(f"{index}. {date} | №{number} | {farmer_name} | Миқдор: {quantity:.2f}")

    text = "\n".join(lines)
    await message.answer(f"<pre>{text}</pre>", parse_mode="HTML", reply_markup=warehouse_menu)


@router.message(F.text.func(lambda value: bool(value)))
@access_required
async def warehouse_item_handler(message: Message):
    warehouse_map = await _warehouse_map()
    selected = (message.text or "").strip()

    warehouse_id = next((wid for wid, name in warehouse_map.items() if name == selected), None)
    if not warehouse_id:
        return

    await message.answer(
        f"🏬 {selected}\nКеракли бўлимни танланг:",
        reply_markup=warehouse_sections_inline_keyboard(warehouse_id),
    )


@router.callback_query(F.data.startswith("warehouse_section:"))
@access_required
async def warehouse_section_handler(callback: CallbackQuery):
    _, warehouse_id, section = callback.data.split(":", maxsplit=2)
    warehouse_id = int(warehouse_id)
    warehouse_map = await _warehouse_map()
    warehouse_name = warehouse_map.get(warehouse_id, "Омбор")

    movement = "in" if section == "receipt" else "out"
    title = "📥 Кирим" if movement == "in" else "📤 Чиқим"

    if movement == "out":
        districts = await get_warehouse_expense_districts(warehouse_id=warehouse_id)
        if not districts:
            await callback.message.edit_text(f"🏬 {warehouse_name}\n\nЧиқим бўйича туманлар топилмади.")
            await callback.answer()
            return

        await callback.message.edit_text(
            f"🏬 {warehouse_name}\n📤 Чиқим учун туманни танланг:",
            reply_markup=warehouse_expense_districts_inline_keyboard(warehouse_id, districts),
        )
        await callback.answer()
        return

    products = await get_warehouse_products(warehouse_id=warehouse_id, movement=movement)

    if not products:
        await callback.message.edit_text(f"🏬 {warehouse_name}\n\n{title} бўйича маълумот топилмади.")
        await callback.answer()
        return

    await callback.message.edit_text(
        f"🏬 {warehouse_name}\n{title} учун маҳсулотни танланг:",
        reply_markup=warehouse_products_inline_keyboard(warehouse_id, movement, products),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("warehouse_expense_district:"))
@access_required
async def warehouse_expense_district_handler(callback: CallbackQuery):
    _, warehouse_id, district_id = callback.data.split(":", maxsplit=2)
    warehouse_id = int(warehouse_id)
    district_id = int(district_id)

    warehouse_map = await _warehouse_map()
    warehouse_name = warehouse_map.get(warehouse_id, "Омбор")
    products = await get_warehouse_products(
        warehouse_id=warehouse_id,
        movement="out",
        district_id=None if district_id == 0 else district_id,
    )

    if not products:
        await callback.message.edit_text(f"🏬 {warehouse_name}\n\n📤 Чиқим бўйича маълумот топилмади.")
        await callback.answer()
        return

    await callback.message.edit_text(
        f"🏬 {warehouse_name}\n📤 Чиқим учун маҳсулотни танланг:",
        reply_markup=warehouse_products_inline_keyboard(warehouse_id, f"out_d{district_id}", products),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("warehouse_product:"))
@access_required
async def warehouse_product_handler(callback: CallbackQuery):
    _, warehouse_id, movement, product_id = callback.data.split(":", maxsplit=3)
    warehouse_id = int(warehouse_id)
    product_id = int(product_id)

    district_id = None
    actual_movement = movement
    if movement.startswith("out_d"):
        actual_movement = "out"
        district_id = int(movement.removeprefix("out_d"))

    totals = await get_warehouse_totals_by_filters(
        warehouse_id=warehouse_id,
        product_id=product_id,
        district_id=district_id,
    )
    movements = await get_warehouse_movements(
        movement=actual_movement,
        warehouse_id=warehouse_id,
        product_id=product_id,
        district_id=district_id,
    )
    warehouse_map = await _warehouse_map()
    warehouse_name = warehouse_map.get(warehouse_id, "Омбор")

    products = await get_warehouse_products(
        warehouse_id=warehouse_id,
        movement=actual_movement,
        district_id=district_id,
    )
    product_name = next(
        (item.get("product_name") for item in products if int(item.get("product_id", 0)) == product_id),
        "Маҳсулот",
    )

    lines = [
        f"🏬 {warehouse_name}",
        f"📦 {product_name}",
        "",
        f"📥 Кирим: {float(totals.get('total_in', 0)):.2f}",
        f"📤 Чиқим: {float(totals.get('total_out', 0)):.2f}",
        f"🧮 Қолдиқ: {float(totals.get('balance', 0)):.2f}",
        "",
    ]

    if actual_movement == "in":
        lines.append("📥 Кирим деталлари:")
        for index, item in enumerate(movements[:30], start=1):
            lines.append(
                f"{index}. {item.get('date') or '-'} | №{item.get('invoice_number') or '-'} | "
                f"миқдори: {float(item.get('quantity') or 0):.2f}"
            )
    else:
        lines.append("📤 Чиқим деталлари:")
        for index, item in enumerate(movements[:30], start=1):
            lines.append(
                f"{index}. {item.get('date') or '-'} | №{item.get('number') or '-'} | "
                f"{item.get('farmer_name') or '-'} | миқдори: {float(item.get('quantity') or 0):.2f}"
            )

    content = "\n".join(lines)
    await callback.message.edit_text(f"<pre>{content}</pre>", parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("warehouse_export:"))
@access_required
async def warehouse_export_handler(callback: CallbackQuery):
    _, warehouse_id, movement = callback.data.split(":", maxsplit=2)
    warehouse_id = int(warehouse_id)
    data = await get_warehouse_movements(movement=movement, warehouse_id=warehouse_id)

    if movement == "in":
        file_buffer = await warehouse_receipts_to_excel(data)
        filename = "warehouse_receipts.xlsx"
    else:
        file_buffer = await warehouse_expenses_to_excel(data)
        filename = "warehouse_expenses.xlsx"

    if not file_buffer:
        await callback.answer("Маълумот йўқ", show_alert=True)
        return

    file = BufferedInputFile(file_buffer.getvalue(), filename=filename)
    await callback.message.answer_document(document=file)
    await callback.answer()

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards import (
    warehouse_menu,
    warehouse_names_menu,
    warehouse_products_inline_keyboard,
    warehouse_sections_inline_keyboard,
)
from tgbot.middlewares.access import access_required
from tgbot.services.api_client import (
    get_warehouse_expenses,
    get_warehouse_products,
    get_warehouse_receipts,
    get_warehouse_totals,
    get_warehouse_totals_by_filters,
    get_warehouses,
)

router = Router()

WAREHOUSE_REPORT_NAMES = {"📊 Ҳисобот", "hisobot", "ҳисобот", "xisobot"}
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


@router.message(F.text.func(lambda value: value and value.lower() in {name.lower() for name in WAREHOUSE_REPORT_NAMES}))
@access_required
async def warehouse_report_handler(message: Message):
    totals = await get_warehouse_totals()

    text = (
        "🏬 Барча омбор бўйича ҳисобот\n\n"
        f"📥 Кирим: {float(totals.get('total_in', 0)):.2f}\n"
        f"📤 Чиқим: {float(totals.get('total_out', 0)):.2f}\n"
        f"🧮 Қолдиқ: {float(totals.get('balance', 0)):.2f}"
    )

    await message.answer(f"<pre>{text}</pre>", parse_mode="HTML", reply_markup=warehouse_menu)


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
        lines.append(f"{index}. {date} | {farmer_name} | Миқдор: {quantity:.2f}")

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

    if section == "report":
        products = await get_warehouse_products(warehouse_id=warehouse_id, movement="all")
        if not products:
            await callback.message.edit_text(f"🏬 {warehouse_name}\n\nМаълумот топилмади.")
            await callback.answer()
            return

        lines = [f"🏬 {warehouse_name}", "📊 Ҳисобот (продукт кесимида)", ""]
        for idx, item in enumerate(products, start=1):
            product_name = item.get("product_name") or "-"
            total_in = float(item.get("total_in") or 0)
            total_out = float(item.get("total_out") or 0)
            balance = float(item.get("balance") or 0)
            lines.append(
                f"{idx}. {product_name}\n"
                f"   📥 {total_in:.2f} | 📤 {total_out:.2f} | 🧮 {balance:.2f}"
            )

        await callback.message.edit_text("\n".join(lines))
        await callback.answer()
        return

    movement = "in" if section == "receipt" else "out"
    title = "📥 Кирим" if movement == "in" else "📤 Чиқим"
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


@router.callback_query(F.data.startswith("warehouse_product:"))
@access_required
async def warehouse_product_handler(callback: CallbackQuery):
    _, warehouse_id, movement, product_id = callback.data.split(":", maxsplit=3)
    warehouse_id = int(warehouse_id)
    product_id = int(product_id)

    totals = await get_warehouse_totals_by_filters(warehouse_id=warehouse_id, product_id=product_id)
    warehouse_map = await _warehouse_map()
    warehouse_name = warehouse_map.get(warehouse_id, "Омбор")

    products = await get_warehouse_products(warehouse_id=warehouse_id, movement=movement)
    product_name = next(
        (item.get("product_name") for item in products if int(item.get("product_id", 0)) == product_id),
        "Маҳсулот",
    )

    text = (
        f"🏬 {warehouse_name}\n"
        f"📦 {product_name}\n\n"
        f"📥 Кирим: {float(totals.get('total_in', 0)):.2f}\n"
        f"📤 Чиқим: {float(totals.get('total_out', 0)):.2f}\n"
        f"🧮 Қолдиқ: {float(totals.get('balance', 0)):.2f}"
    )

    await callback.message.edit_text(text)
    await callback.answer()

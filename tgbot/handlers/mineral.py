from aiogram import Router, F
from aiogram.types import Message

from tgbot.keyboards import warehouse_menu, warehouse_names_menu
from tgbot.middlewares.access import access_required
from tgbot.services.api_client import (
    get_warehouse_totals,
    get_warehouse_receipts,
    get_warehouse_expenses,
    get_warehouses,
)

router = Router()

WAREHOUSE_REPORT_NAMES = {"📊 Ҳисобот", "hisobot", "ҳисобот", "xisobot"}
WAREHOUSE_RECEIPT_NAMES = {"📥 Кирим", "kirim", "krim", "кирим"}
WAREHOUSE_EXPENSE_NAMES = {"📤 Чиқим", "chiqim", "чиқим"}


@router.message(F.text.in_({"🌾 Минерал ўғит", "🏬 Омбор"}))
@access_required
async def mineral_menu_handler(message: Message):
    warehouses = await get_warehouses()
    warehouse_names = [str(item.get("name", "")).strip() for item in warehouses]

    if not any(warehouse_names):
        await message.answer(
            "Омборлар топилмади. Қуйидаги тугмалардан фойдаланинг 👇",
            reply_markup=warehouse_menu,
        )
        return

    await message.answer(
        "🏬 Омбор\n\nWarehouse modeldagi номлар 👇",
        reply_markup=warehouse_names_menu(warehouse_names),
    )


@router.message(F.text.func(lambda value: value and value.lower() in {name.lower() for name in WAREHOUSE_REPORT_NAMES}))
@access_required
async def warehouse_report_handler(message: Message):
    totals = await get_warehouse_totals()

    text = (
        "🏬 Минерал ўғит омбори ҳисоботи\n\n"
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

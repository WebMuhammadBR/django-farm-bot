from aiogram import Router, F
from aiogram.types import Message

from tgbot.keyboards import mineral_menu, warehouse_menu
from tgbot.middlewares.access import access_required
from tgbot.services.api_client import (
    get_warehouse_totals,
    get_warehouse_receipts,
    get_warehouse_expenses,
    get_warehouses,
)

router = Router()


@router.message(F.text.in_({"🌾 Минерал ўғит", "🏬 Омбор"}))
@access_required
async def mineral_menu_handler(message: Message):
    await message.answer("Омбор бўлими 👇", reply_markup=mineral_menu)


@router.message(F.text.in_({"🌾 Оғит омбор", "🌾 Оғит омбор (барча Warehouse)", "🌾 Минерал ўғит омбори"}))
@access_required
async def warehouse_summary_handler(message: Message):
    await message.answer(
        "🌾 Оғит омбори\n\nҚуйидаги тугмалардан керакли бўлимни танланг 👇",
        reply_markup=warehouse_menu,
    )



@router.message(F.text == "📊 Ҳисобот")
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


@router.message(F.text == "📥 Кирим")
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


@router.message(F.text == "📤 Чиқим")
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


@router.message(F.text == "🧾 Омборлар")
@access_required
async def warehouse_list_handler(message: Message):
    warehouses = await get_warehouses()

    if not warehouses:
        await message.answer("Омборлар рўйхати бўш", reply_markup=warehouse_menu)
        return

    lines = ["🧾 Омборлар рўйхати (Warehouse)", ""]

    for index, item in enumerate(warehouses, start=1):
        lines.append(f"{index}. ID: {item.get('id', '-') } | Номи: {item.get('name', '-')}")

    text = "\n".join(lines)
    await message.answer(f"<pre>{text}</pre>", parse_mode="HTML", reply_markup=warehouse_menu)

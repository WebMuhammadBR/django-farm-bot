from aiogram import Router, F
from aiogram.types import Message

from tgbot.keyboards import mineral_menu, warehouse_menu
from tgbot.middlewares.access import access_required
from tgbot.services.api_client import (
    get_warehouse_totals,
    get_warehouse_receipts,
    get_warehouse_expenses,
)

router = Router()


@router.message(F.text == "🌾 Минерал ўғит")
@access_required
async def mineral_menu_handler(message: Message):
    await message.answer("Минерал ўғит бўлими 👇", reply_markup=mineral_menu)


@router.message(F.text == "🏬 Омбор")
@access_required
async def warehouse_summary_handler(message: Message):
    totals = await get_warehouse_totals()

    text = (
        "🏬 Омбор ҳисоботи\n\n"
        f"📥 Умумий кирим (миқдор): {float(totals.get('total_in', 0)):.2f}\n"
        f"📤 Умумий чиқим (миқдор): {float(totals.get('total_out', 0)):.2f}\n"
        f"🧮 Қолдиқ (миқдор): {float(totals.get('balance', 0)):.2f}\n\n"
        f"💰 Умумий кирим (сумма): {float(totals.get('total_in_amount', 0)):.2f}\n"
        f"💸 Умумий чиқим (сумма): {float(totals.get('total_out_amount', 0)):.2f}\n"
        f"💵 Қолдиқ (сумма): {float(totals.get('balance_amount', 0)):.2f}"
    )

    await message.answer(text, reply_markup=warehouse_menu)


@router.message(F.text == "📥 Кирим")
@access_required
async def warehouse_receipts_handler(message: Message):
    receipts = await get_warehouse_receipts()

    if not receipts:
        await message.answer("Кирим рўйхати бўш", reply_markup=warehouse_menu)
        return

    lines = ["📥 Омбор кирим рўйхати", ""]
    for index, item in enumerate(receipts[:30], start=1):
        lines.append(
            f"{index}. {item['date']} | {item['warehouse']} | №{item['invoice_number']}\n"
            f"   🚚 {item['transport_type_display']} ({item['transport_number']}) | Қоп: {item['bag_count']}\n"
            f"   📦 {item['product']} | Миқдор: {float(item['quantity']):.2f} | Нарх: {float(item['price']):.2f} | Сумма: {float(item['amount']):.2f}"
        )

    await message.answer("\n".join(lines), reply_markup=warehouse_menu)


@router.message(F.text == "📤 Чиқим")
@access_required
async def warehouse_expenses_handler(message: Message):
    expenses = await get_warehouse_expenses()

    if not expenses:
        await message.answer("Чиқим рўйхати бўш", reply_markup=warehouse_menu)
        return

    lines = ["📤 Омбор чиқим рўйхати", ""]
    for index, item in enumerate(expenses[:30], start=1):
        warehouse_name = item.get("warehouse_name") or "-"
        lines.append(
            f"{index}. {item['date']} | {warehouse_name} | №{item['number']} | Сумма: {float(item['total_amount']):.2f}"
        )

    await message.answer("\n".join(lines), reply_markup=warehouse_menu)

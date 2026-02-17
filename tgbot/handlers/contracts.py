from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from urllib.parse import unquote

from tgbot.services.api_client import get_contracts_summary
from tgbot.excel_export import contracts_to_excel
from tgbot.keyboards import contracts_filter_keyboard, contracts_pagination_keyboard
from tgbot.middlewares.access import access_required
from tgbot.services.pagination import build_page_text, paginate_data

router = Router()
PER_PAGE = 25


@router.message(F.text == "📑 Шартномалар")
@access_required
async def contracts_handler(message: Message):
    data = await get_contracts_summary()
    districts = extract_districts(data)
    await message.answer("Туманни танланг 👇", reply_markup=contracts_filter_keyboard(districts))


@router.callback_query(F.data.startswith("contracts_filter:"))
@access_required
async def contracts_pagination(callback: CallbackQuery):
    _, district, page = callback.data.split(":", 2)
    district = unquote(district)
    await send_page(callback.message, int(page), district, True)
    await callback.answer()


@router.callback_query(F.data == "contracts_back_to_filters")
@access_required
async def contracts_back_to_filters(callback: CallbackQuery):
    data = await get_contracts_summary()
    districts = extract_districts(data)
    await callback.message.edit_text("Туманни танланг 👇", reply_markup=contracts_filter_keyboard(districts))
    await callback.answer()


async def send_page(target, page, district, edit):
    data = await get_contracts_summary()
    filtered_data = filter_by_district(data, district)
    page_data, start, end = paginate_data(filtered_data, page, PER_PAGE)

    district_title = "Умумий" if district == "all" else district

    text = build_page_text(
        title=f"📑 Шартномалар: {district_title}",
        headers=f"{'№':<3} {'Фермер номи':<14} {'миқдор':>5} {'Сумма':>8}",
        subheaders=f"{' ':<3} {'   ':<15} {'(тн)':>5} {'(млн)':>9}",
        rows=[
            (
                f"{index:<3} "
                f"{contract['name'][:15]:<15} "
                f"{float(contract['quantity']):>5,.1f}"
                f"{float(contract['amount']):>12,.0f}"
            )
            for index, contract in enumerate(page_data, start=start + 1)
        ],
    )

    keyboard = contracts_pagination_keyboard(page, end < len(filtered_data), district)

    if edit:
        await target.edit_text(f"<pre>{text}</pre>", parse_mode="HTML", reply_markup=keyboard)
    else:
        await target.answer(f"<pre>{text}</pre>", parse_mode="HTML", reply_markup=keyboard)


@router.callback_query(F.data.startswith("contracts_export_excel:"))
@access_required
async def contracts_excel(callback: CallbackQuery):
    district = unquote(callback.data.split(":", 1)[1])
    data = await get_contracts_summary()
    filtered_data = filter_by_district(data, district)

    file_buffer = await contracts_to_excel(filtered_data)

    if not file_buffer:
        await callback.answer("Маълумот йўқ", show_alert=True)
        return

    file = BufferedInputFile(
        file_buffer.getvalue(),
        filename="contracts.xlsx"
    )

    await callback.message.answer_document(
        document=file
    )

    await callback.answer()


def extract_districts(data: list[dict]) -> list[str]:
    districts = {
        contract.get("district")
        for contract in data
        if contract.get("district")
    }
    return sorted(districts)


def filter_by_district(data: list[dict], district: str) -> list[dict]:
    if district == "all":
        return data
    return [contract for contract in data if contract.get("district") == district]

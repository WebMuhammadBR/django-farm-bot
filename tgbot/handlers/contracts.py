from aiogram import F, Router
from aiogram.types import BufferedInputFile, CallbackQuery, Message

from tgbot.excel_export import contracts_to_excel
from tgbot.keyboards import contracts_filters_keyboard, contracts_pagination_keyboard
from tgbot.middlewares.access import access_required
from tgbot.services.api_client import get_contracts_summary
from tgbot.services.pagination import build_page_text, paginate_data

router = Router()
PER_PAGE = 25


@router.message(F.text == "📑 Шартномалар")
@access_required
async def contracts_handler(message: Message):
    await message.answer("Шартнома бўлими. Туманни танланг 👇", reply_markup=contracts_filters_keyboard(await get_districts()))


@router.callback_query(F.data == "contracts_back:filters")
@access_required
async def contracts_back_to_filters(callback: CallbackQuery):
    await callback.message.edit_text(
        "Шартнома бўлими. Туманни танланг 👇",
        reply_markup=contracts_filters_keyboard(await get_districts()),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("contracts_filter:"))
@access_required
async def contracts_filter_selected(callback: CallbackQuery):
    parts = callback.data.split(":")
    if parts[1] == "all":
        filter_token = "all"
    else:
        filter_token = f"district:{parts[2]}"

    await send_page(callback.message, page=1, edit=True, filter_token=filter_token)
    await callback.answer()


@router.callback_query(F.data.startswith("contracts_page:"))
@access_required
async def contracts_pagination(callback: CallbackQuery):
    _, page, filter_token = callback.data.split(":", 2)
    await send_page(callback.message, page=int(page), edit=True, filter_token=filter_token)
    await callback.answer()


async def send_page(target, page: int, edit: bool, filter_token: str):
    data = await get_contracts_summary()
    filtered_data = apply_filter(data, filter_token)
    page_data, start, end = paginate_data(filtered_data, page, PER_PAGE)

    text = build_page_text(
        title="📑 Шартномалар рўйхати",
        headers=f"{'№':<3} {'Фермер номи':<14} {'миқдор':>5} {'Сумма':>8}",
        subheaders=f"{' ':<3} {'     ':<15} {'(тн)':>5} {'(млн)':>9}",
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

    keyboard = contracts_pagination_keyboard(page, end < len(filtered_data), filter_token)

    if edit:
        await target.edit_text(f"<pre>{text}</pre>", parse_mode="HTML", reply_markup=keyboard)
    else:
        await target.answer(f"<pre>{text}</pre>", parse_mode="HTML", reply_markup=keyboard)


@router.callback_query(F.data.startswith("contracts_export_excel:"))
@access_required
async def contracts_excel(callback: CallbackQuery):
    filter_token = callback.data.split(":", 1)[1]
    data = apply_filter(await get_contracts_summary(), filter_token)
    file_buffer = await contracts_to_excel(data)

    if not file_buffer:
        await callback.answer("Маълумот йўқ", show_alert=True)
        return

    file = BufferedInputFile(file_buffer.getvalue(), filename="contracts.xlsx")
    await callback.message.answer_document(document=file)
    await callback.answer()



def apply_filter(data: list[dict], filter_token: str):
    if filter_token == "all":
        return data

    if not filter_token.startswith("district:"):
        return data

    districts = sorted({item.get("district") for item in data if item.get("district")})

    try:
        district_index = int(filter_token.split(":", 1)[1])
        district_name = districts[district_index]
    except (ValueError, IndexError):
        return data

    return [item for item in data if item.get("district") == district_name]


async def get_districts():
    data = await get_contracts_summary()
    return sorted({item.get("district") for item in data if item.get("district")})

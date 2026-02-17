from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from tgbot.services.api_client import get_contracts_summary
from tgbot.excel_export import contracts_to_excel
from tgbot.keyboards import contracts_pagination_keyboard
from tgbot.middlewares.access import access_required
from tgbot.services.pagination import build_page_text, paginate_data

router = Router()
PER_PAGE = 25


@router.message(F.text == "📑 Шартномалар")
@access_required
async def contracts_handler(message: Message):
    await send_page(message, 1, False)


@router.callback_query(F.data.startswith("contracts_page:"))
@access_required
async def contracts_pagination(callback: CallbackQuery):
    page = int(callback.data.split(":")[1])
    await send_page(callback.message, page, True)
    await callback.answer()


async def send_page(target, page, edit):
    data = await get_contracts_summary()
    page_data, start, end = paginate_data(data, page, PER_PAGE)

    text = build_page_text(
        title="📑 Шартномалар рўйхати",
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

    keyboard = contracts_pagination_keyboard(page, end < len(data))

    if edit:
        await target.edit_text(f"<pre>{text}</pre>", parse_mode="HTML", reply_markup=keyboard)
    else:
        await target.answer(f"<pre>{text}</pre>", parse_mode="HTML", reply_markup=keyboard)


@router.callback_query(F.data == "contracts_export_excel")
@access_required
async def contracts_excel(callback: CallbackQuery):
    data = await get_contracts_summary()

    file_buffer = await contracts_to_excel(data)

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

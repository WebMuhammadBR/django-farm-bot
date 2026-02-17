from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from tgbot.services.api_client import get_farmers
from tgbot.excel_export import farmers_to_excel
from tgbot.keyboards import farmers_pagination_keyboard
from tgbot.middlewares.access import access_required
from tgbot.services.pagination import build_page_text, paginate_data

router = Router()
PER_PAGE = 25


@router.message(F.text == "📋 Фермерлар рўйхати")
@access_required
async def farmers_handler(message: Message):
    await send_page(message, 1, False)


@router.callback_query(F.data.startswith("farmers_page:"))
@access_required
async def farmers_pagination(callback: CallbackQuery):
    page = int(callback.data.split(":")[1])
    await send_page(callback.message, page, True)
    await callback.answer()


async def send_page(target, page, edit):
    data = await get_farmers()
    page_data, start, end = paginate_data(data, page, PER_PAGE)

    text = build_page_text(
        title="📋 Фермерлар рўйхати",
        headers=f"{'№':<3} {'Фермер номи':<18} {'Баланс':>13}",
        rows=[
            f"{index:<3} {farmer['name'][:18]:<18} {float(farmer['balance']):>13,.1f}"
            for index, farmer in enumerate(page_data, start=start + 1)
        ],
    )
    keyboard = farmers_pagination_keyboard(page, end < len(data))

    if edit:
        await target.edit_text(f"<pre>{text}</pre>", parse_mode="HTML", reply_markup=keyboard)
    else:
        await target.answer(f"<pre>{text}</pre>", parse_mode="HTML", reply_markup=keyboard)


@router.callback_query(F.data == "farmers_export_excel")
@access_required
async def farmers_excel(callback: CallbackQuery):
    data = await get_farmers()

    file_buffer = await farmers_to_excel(data)

    if not file_buffer:
        await callback.answer("Маълумот йўқ", show_alert=True)
        return

    file = BufferedInputFile(
        file_buffer.getvalue(),
        filename="farmers.xlsx"
    )

    await callback.message.answer_document(
        document=file
    )

    await callback.answer()

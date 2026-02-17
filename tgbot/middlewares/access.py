from functools import wraps
from aiogram.types import Message, CallbackQuery
from tgbot.services.api_client import check_access


def access_required(handler):

    @wraps(handler)
    async def wrapper(event, *args, **kwargs):

        if isinstance(event, Message):
            telegram_id = event.from_user.id
            full_name = event.from_user.full_name
        elif isinstance(event, CallbackQuery):
            telegram_id = event.from_user.id
            full_name = event.from_user.full_name
        else:
            return

        result = await check_access(telegram_id, full_name)

        if not result["allowed"]:
            if isinstance(event, Message):
                await event.answer("⛔️ Сизга рухсат берилмаган.")
            else:
                await event.answer("⛔️ Рухсат йўқ", show_alert=True)
            return

        return await handler(event, *args, **kwargs)

    return wrapper

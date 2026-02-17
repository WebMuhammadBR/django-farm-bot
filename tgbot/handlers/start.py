from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from tgbot.keyboards import main_menu
from tgbot.middlewares.access import access_required

router = Router()


@router.message(CommandStart())
@access_required
async def start_handler(message: Message):
    await message.answer("Асосий меню 👇", reply_markup=main_menu)

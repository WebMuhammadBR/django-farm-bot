from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards import main_menu
from tgbot.middlewares.access import access_required

router = Router()


@router.message(CommandStart())
@access_required
async def start_handler(message: Message):
    await message.answer("Асосий меню 👇", reply_markup=main_menu)


@router.callback_query(F.data == "menu:main")
@access_required
async def main_menu_handler(callback: CallbackQuery):
    await callback.message.answer("Асосий меню 👇", reply_markup=main_menu)
    await callback.answer()

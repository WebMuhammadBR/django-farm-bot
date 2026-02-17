import asyncio
from aiogram import Bot, Dispatcher

from tgbot.config import TOKEN
from tgbot.handlers import start, farmers, contracts

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(farmers.router)
dp.include_router(contracts.router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

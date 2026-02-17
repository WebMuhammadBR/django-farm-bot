import aiohttp
from tgbot.config import API_BASE_URL


async def check_access(telegram_id: int, full_name: str):

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE_URL}/bot-user/check/",
            json={
                "telegram_id": telegram_id,
                "full_name": full_name
            }
        ) as resp:
            return await resp.json()


async def get_farmers():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/farmers/") as resp:
            return await resp.json()


async def get_contracts_summary():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/farmers/summary/") as resp:
            return await resp.json()

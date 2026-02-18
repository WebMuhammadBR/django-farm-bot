from urllib.parse import urlencode

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


async def get_warehouse_totals():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/warehouse/totals/") as resp:
            return await resp.json()


async def get_warehouse_receipts():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/warehouse/receipts/") as resp:
            return await resp.json()


async def get_warehouse_expenses():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/warehouse/expenses/") as resp:
            return await resp.json()


async def get_warehouses():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/warehouse/list/") as resp:
            return await resp.json()


async def get_warehouse_totals_by_filters(warehouse_id: int | None = None, product_id: int | None = None):
    params = {}
    if warehouse_id:
        params["warehouse_id"] = warehouse_id
    if product_id:
        params["product_id"] = product_id

    query = f"?{urlencode(params)}" if params else ""

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/warehouse/totals/{query}") as resp:
            return await resp.json()


async def get_warehouse_products(warehouse_id: int | None = None, movement: str | None = None):
    params = {}
    if warehouse_id:
        params["warehouse_id"] = warehouse_id
    if movement:
        params["movement"] = movement

    query = f"?{urlencode(params)}" if params else ""

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/warehouse/products/{query}") as resp:
            return await resp.json()


async def get_warehouse_movements(
    movement: str,
    warehouse_id: int | None = None,
    product_id: int | None = None,
):
    params = {"movement": movement}
    if warehouse_id:
        params["warehouse_id"] = warehouse_id
    if product_id:
        params["product_id"] = product_id

    query = f"?{urlencode(params)}" if params else ""

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/warehouse/movements/{query}") as resp:
            return await resp.json()

from typing import Any

from beanie import init_beanie
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from bot.binancerequests import get_cur_price_api
from bot.config import settings
from bot.dbmodels import Task


async def init_db() -> None:
    client = AsyncIOMotorClient(settings.MONGO_URL)
    await init_beanie(database=client[settings.MONGO_DB], document_models=[Task])


async def get_task_db(user_id: int, tickers_pair: str) -> Task | None:
    return await Task.find(Task.user_id == user_id, Task.tickers_pair == tickers_pair).first_or_none()


async def count_tasks_db(user_id: int) -> int:
    return await Task.find(Task.user_id == user_id).count()


async def get_all_users_tasks_db(user_id: int) -> list[Task]:
    return await Task.find(Task.user_id == user_id).to_list()


async def create_task_db(user_id: int, task_data: dict[str, Any], interval: int) -> Task:
    tickers_pair = task_data['first_ticker'] + task_data['second_ticker']
    current_price = await get_cur_price_api(tickers_pair=tickers_pair)
    new_task = Task(user_id=user_id,
                    tickers_pair=tickers_pair,
                    interval_minutes=interval,
                    percentage=float(task_data['percentage']),
                    price=float(current_price))
    return await Task.insert_one(new_task)


async def upd_task_price_db(task: Task, new_price: float) -> None:
    task.price = new_price
    await task.save()


async def del_task_db(task_id: str | ObjectId) -> None:
    await Task.find_one(Task.id == ObjectId(task_id)).delete()

from aiogram import Bot
from aiogram.enums import ParseMode
from pytz import utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.base import JobLookupError

from bot.binancerequests import get_cur_price_api
from bot.constants import PAIR_UP, PAIR_DOWN
from bot.dbmodels import Task
from bot.dbservice import upd_task_price_db
from bot.config import settings


job_stores = {'default': RedisJobStore(db=settings.REDIS_JOB_DB,
                                       host=settings.REDIS_HOST,
                                       port=int(settings.REDIS_PORT))}


executors = {'default': AsyncIOExecutor()}

job_defaults = {'coalesce': False, 'max_instances': 3}

scheduler = AsyncIOScheduler(jobstores=job_stores, executors=executors, job_defaults=job_defaults, timezone=utc)


async def send_changed_price(task: Task) -> None:
    bot = Bot(settings.BOT_API_TOKEN, parse_mode=ParseMode.HTML)
    cur_price = float(await get_cur_price_api(tickers_pair=task.tickers_pair))
    delta = cur_price - task.price
    cur_percentage = 100*delta/cur_price

    if cur_percentage >= task.percentage:
        await bot.send_message(chat_id=task.user_id,
                               text=PAIR_UP.format(tickers_pair=task.tickers_pair,
                                                   percentage=str(task.percentage),
                                                   current_price=cur_price))

    if cur_percentage <= -task.percentage:
        await bot.send_message(chat_id=task.user_id,
                               text=PAIR_DOWN.format(tickers_pair=task.tickers_pair,
                                                     percentage=str(task.percentage),
                                                     current_price=cur_price))

    await upd_task_price_db(task=task, new_price=cur_price)
    await bot.session.close()


async def start_scheduler() -> None:
    scheduler.start()


async def shutdown_scheduler() -> None:
    scheduler.shutdown()


async def create_job(interval: int, job_id: str, task: Task) -> None:
    scheduler.add_job(func=send_changed_price,
                      trigger='interval',
                      minutes=interval,
                      id=job_id,
                      kwargs={'task': task})


async def del_job(job_id: str) -> None:
    try:
        scheduler.remove_job(job_id=job_id)
    except JobLookupError:
        return

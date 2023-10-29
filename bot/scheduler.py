from aiogram import Bot
from pytz import utc

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler_di import ContextSchedulerDecorator

from bot.db import gettaskbytickers, addnewcurrentprice
from bot.binancerequests import getcurrentprice
from bot.config import REDISHOST, REDISPORT, REDISTASKSDB, APITOKEN
from bot.dbmodels import UserTask
from bot.constants import PAIRUP, PAIRDOWN


job_stores = {'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
                                       run_times_key='dispatched_trips_running',
                                       host=REDISHOST,
                                       port=REDISPORT,
                                       db=REDISTASKSDB)}

executors = {'default': AsyncIOExecutor()}

job_defaults = {'coalesce': False,
                'max_instances': 3}

scheduler = ContextSchedulerDecorator(AsyncIOScheduler(jobstores=job_stores,
                                                       executors=executors,
                                                       job_defaults=job_defaults,
                                                       timezone=utc))


async def sendchangedcur(userid: int, task: UserTask) -> None:
    bot = Bot(APITOKEN)
    session = await bot.get_session()
    currenttask = await gettaskbytickers(userid=userid,
                                         firtick=task.firstticker,
                                         sectick=task.secondticker)
    currentprice = await getcurrentprice(firtick=task.firstticker,
                                         sectick=task.secondticker)
    if currenttask and currentprice:
        floatprice = float(currentprice)
        delta = floatprice - currenttask.price
        currentpercent = 100*delta/floatprice
        if currentpercent > task.percentofchange:
            await bot.send_message(chat_id=userid,
                                   text=PAIRUP.format(firstticker=task.firstticker,
                                                      secondticker=task.secondticker,
                                                      currentprice=currentprice),
                                   parse_mode='HTML')
        elif currentpercent < -task.percentofchange:
            await bot.send_message(chat_id=userid,
                                   text=PAIRDOWN.format(firstticker=task.firstticker,
                                                        secondticker=task.secondticker,
                                                        currentprice=currentprice),
                                   parse_mode='HTML')
        await addnewcurrentprice(task=currenttask, currentprice=floatprice)
    await session.close()


async def addscheduler(userid: int, time: int, task: UserTask) -> None:
    scheduler.add_job(func=sendchangedcur,
                      trigger='interval',
                      minutes=time,
                      id=str(task.id),
                      kwargs=dict(userid=userid, task=task))


async def removescheduler(schedid: str) -> None:
    scheduler.remove_job(job_id=schedid)

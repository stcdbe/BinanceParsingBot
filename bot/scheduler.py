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

jobstores = {'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
                                      run_times_key='dispatched_trips_running',
                                      host=REDISHOST,
                                      port=REDISPORT,
                                      db=REDISTASKSDB)}

executors = {'default': AsyncIOExecutor()}

job_defaults = {'coalesce': False,
                'max_instances': 3}

scheduler = ContextSchedulerDecorator(AsyncIOScheduler(jobstores=jobstores,
                                                       executors=executors,
                                                       job_defaults=job_defaults,
                                                       timezone=utc))


async def sendchangedcurrency(userid: int, task: UserTask) -> None:
    bot = Bot(APITOKEN)
    session = await bot.get_session()
    currenttask = await gettaskbytickers(userid=userid, firstticker=task.firstticker, secondticker=task.secondticker)
    currentprice = await getcurrentprice(firstticker=task.firstticker, secondticker=task.secondticker)
    if currenttask and currentprice:
        floatprice = float(currentprice)
        delta = floatprice - currenttask.price
        currentpercent = 100*delta/floatprice
        if currentpercent > task.percentofchange:
            await bot.send_message(chat_id=userid,
                                   text=f'Pair <b>{task.firstticker}/{task.secondticker}</b> rose above the set'
                                        f' percentage.\n\nCurrent price: <b>{currentprice}</b>',
                                   parse_mode='HTML')
        elif currentpercent < -task.percentofchange:
            await bot.send_message(chat_id=userid,
                                   text=f'Pair <b>{task.firstticker}/{task.secondticker}</b> fell below the set'
                                        f' percentage.\n\nCurrent price: <b>{currentprice}</b>',
                                   parse_mode='HTML')
        else:
            pass
        await addnewcurrentprice(task=currenttask, currentprice=floatprice)
    else:
        pass
    await session.close()


async def addscheduler(userid: int, time: int, task: UserTask) -> None:
    schedulerid = str(task.id)
    scheduler.add_job(func=sendchangedcurrency,
                      trigger='interval',
                      minutes=time,
                      id=schedulerid,
                      kwargs={'userid': userid, 'task': task})


async def removescheduler(schedulerid: str) -> None:
    scheduler.remove_job(job_id=schedulerid)

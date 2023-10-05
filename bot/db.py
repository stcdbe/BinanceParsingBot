from typing import Sequence
from uuid import UUID

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from bot.dbmodels import DBBaseModel, UserTask
from bot.binancerequests import getcurrentprice
from bot.config import PGUSER, PGPORT, PGPASSWORD, PGDB, PGHOST


DATABASEURI = f'postgresql+asyncpg://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDB}'
# DATABASEURI = 'sqlite+aiosqlite:///binancebot.db'

async_engine = create_async_engine(url=DATABASEURI,
                                   echo=False,
                                   pool_pre_ping=True)

async_session = async_sessionmaker(bind=async_engine,
                                   expire_on_commit=False,
                                   class_=AsyncSession)

session = async_session()


async def opendb() -> None:
    async with async_engine.begin() as engine:
        await engine.run_sync(DBBaseModel.metadata.create_all)


async def closedb() -> None:
    await async_engine.dispose()


async def addtasktodb(callback: CallbackQuery, state: FSMContext) -> str | UserTask:
    async with state.proxy() as data:
        firstticker: str = data['firstticker']
        secondticker: str = data['secondticker']
        percentofchange: float = data['percentofchange']
    tasktocheck = (await session.execute(select(UserTask)
                                         .where(and_(UserTask.userid == callback.from_user.id,
                                                     UserTask.firstticker == firstticker,
                                                     UserTask.secondticker == secondticker)))).scalars().first()
    lenoftasks = (await session.execute(select(UserTask)
                                        .where(UserTask.userid == callback.from_user.id))).scalars().all()
    await session.commit()
    if tasktocheck:
        return 'taskexists'
    elif len(lenoftasks) >= 5:
        return 'toomanytasks'
    else:
        currentprice = await getcurrentprice(firtick=firstticker,
                                             sectick=secondticker)
        if currentprice:
            newtask = UserTask(userid=callback.from_user.id,
                               firstticker=firstticker,
                               secondticker=secondticker,
                               percentofchange=percentofchange,
                               price=float(currentprice),)
            session.add(newtask)
            await session.commit()
            return newtask
        return 'taskexists'


async def gettaskbytickers(userid: int,
                           firtick: str,
                           sectick: str) -> UserTask | None:
    tasktoget = (await session.execute(select(UserTask)
                                       .where(and_(UserTask.userid == userid,
                                                   UserTask.firstticker == firtick,
                                                   UserTask.secondticker == sectick)))).scalars().first()
    await session.commit()
    return tasktoget


async def addnewcurrentprice(task: UserTask, currentprice: float) -> None:
    task.price = currentprice
    await session.commit()


async def getusertasks(userid: int) -> Sequence[UserTask]:
    tasks = (await session.execute(select(UserTask)
                                   .where(UserTask.userid == userid))).scalars().all()
    await session.commit()
    return tasks


async def removetaskfromdb(id: UUID) -> None:
    tasktodelete = (await session.execute(select(UserTask)
                                          .where(UserTask.id == id))).scalars().first()
    await session.delete(tasktodelete)
    await session.commit()

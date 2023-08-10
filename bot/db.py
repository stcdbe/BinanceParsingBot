from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from bot.dbmodels import DBBaseModel, UserTask
from bot.binancerequests import getcurrentprice
from bot.config import PGUSER, PGPORT, PGPASSWORD, PGDB, PGHOST


DATABASEURI = f'postgresql+asyncpg://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDB}'

async_engine = create_async_engine(url=DATABASEURI, echo=False)

async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)

session = async_session()


async def opendb() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(DBBaseModel.metadata.create_all)


async def closedb() -> None:
    await async_engine.dispose()


async def addtasktodb(callback: CallbackQuery, state: FSMContext) -> str | UserTask:
    async with state.proxy() as data:
        firstticker: str = data['firstticker']
        secondticker: str = data['secondticker']
        percentofchange: float = data['percentofchange']
    tasktocheck = (await session.execute(select(UserTask).where(UserTask.userid == callback.from_user.id,
                                                                UserTask.firstticker == firstticker,
                                                                UserTask.secondticker == secondticker))
                   ).scalars().first()
    lenoftasks = (await session.execute(select(UserTask).where(UserTask.userid == callback.from_user.id))
                  ).scalars().all()
    if tasktocheck:
        await session.commit()
        return 'taskexists'
    elif len(lenoftasks) >= 2:
        await session.commit()
        return 'toomanytasks'
    else:
        currentprice = await getcurrentprice(firstticker=firstticker, secondticker=secondticker)
        if currentprice:
            newtask = UserTask(userid=callback.from_user.id,
                               firstticker=firstticker,
                               secondticker=secondticker,
                               percentofchange=percentofchange,
                               price=float(currentprice),)
            session.add(newtask)
            await session.commit()
            return newtask
        else:
            await session.commit()
            return 'taskexists'


async def gettaskbytickers(userid: int, firstticker: str, secondticker: str) -> UserTask | None:
    tasktoget = (await session.execute(select(UserTask).where(UserTask.userid == userid,
                                                              UserTask.firstticker == firstticker,
                                                              UserTask.secondticker == secondticker))
                 ).scalars().first()
    await session.commit()
    return tasktoget


async def addnewcurrentprice(task: UserTask, currentprice: float) -> None:
    task.price = currentprice
    await session.commit()


async def getusertasks(userid: int) -> Sequence[UserTask]:
    tasks = (await session.execute(select(UserTask).where(UserTask.userid == userid))
             ).scalars().all()
    await session.commit()
    return tasks


async def removetaskfromdb(id: str) -> None:
    tasktodelete = (await session.execute(select(UserTask).where(UserTask.id == id))
                    ).scalars().first()
    await session.delete(tasktodelete)
    await session.commit()

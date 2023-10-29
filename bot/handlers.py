from aiogram.types import Message, CallbackQuery, Update, ReplyKeyboardRemove, ChatMemberUpdated
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked

from bot.keyboards import getstartkb, gettimekb, gettaskskb
from bot.binancerequests import getcurrentprice
from bot.statesgroups import CoinStates
from bot.db import opendb, closedb, addtasktodb, getusertasks, removetaskfromdb
from bot.scheduler import scheduler, addscheduler, removescheduler
from bot.constants import (STARTMESSAGE,
                           GETFIRSTTICKER,
                           GETSECONDTICKER,
                           CHECKCOINS,
                           CHECKCOINSFAIL,
                           GETPERCENTAGE,
                           TASKEXISTS,
                           TOOMANYTASKS,
                           TASKADDED,
                           SHOWALLTASKS,
                           NOTASKS,
                           REMOVETASK,
                           GETHELP)


async def on_startup(_) -> None:
    await opendb()
    scheduler.start()


async def on_shutdown(_) -> None:
    scheduler.shutdown()
    await closedb()


async def startmes(message: Message) -> None:
    await message.answer(text=STARTMESSAGE)


async def getfirstticker(message: Message) -> None:
    await message.answer(text=GETFIRSTTICKER,
                         reply_markup=await getstartkb())
    await CoinStates.firstticker.set()


async def getsecondticker(message: Message, state: FSMContext) -> None:
    fisrtticker = message.text.upper()
    async with state.proxy() as data:
        data['firstticker'] = fisrtticker
    await message.answer(text=GETSECONDTICKER.format(ticker=fisrtticker),
                         reply_markup=await getstartkb(),
                         parse_mode='HTML')
    await CoinStates.next()


async def checkcoin(message: Message, state: FSMContext) -> None:
    secondticker = message.text.upper()
    async with state.proxy() as data:
        data['secondticker'] = secondticker
        firstticker: str = data['firstticker']
    coinprice = await getcurrentprice(firtick=firstticker, sectick=secondticker)
    if coinprice:
        await CoinStates.next()
        await message.answer(text=CHECKCOINS.format(firstticker=firstticker,
                                                    secondticker=secondticker,
                                                    coinprice=coinprice),
                             reply_markup=ReplyKeyboardRemove(),
                             parse_mode='HTML')
    else:
        await message.answer(text=CHECKCOINSFAIL.format(firstticker=firstticker,
                                                        secondticker=secondticker),
                             reply_markup=ReplyKeyboardRemove(),
                             parse_mode='HTML')
        await state.finish()


async def getcoinpercent(message: Message, state: FSMContext) -> None:
    percent = float(message.text)
    async with state.proxy() as data:
        data['percentofchange'] = percent
    await CoinStates.next()
    await message.answer(text=GETPERCENTAGE.format(percent=percent),
                         reply_markup=await gettimekb(),
                         parse_mode='HTML')


async def getcointime(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    time = int(callback.data.split('_')[1])
    checktask = await addtasktodb(state=state, callback=callback)
    if checktask == 'taskexists':
        await callback.message.answer(text=TASKEXISTS)
    elif checktask == 'toomanytasks':
        await callback.message.answer(text=TOOMANYTASKS)
    else:
        await addscheduler(userid=callback.from_user.id,
                           time=time,
                           task=checktask)
        await callback.message.answer(text=TASKADDED.format(time=str(time)),
                                      parse_mode='HTML')
    await state.finish()


async def cancelstate(message: Message, state: FSMContext) -> None:
    await message.answer(text='Action canceled.', reply_markup=ReplyKeyboardRemove())
    await state.finish()


async def showalltasks(message: Message) -> None:
    tasks = await getusertasks(userid=message.from_user.id)
    if tasks:
        await message.answer(text=SHOWALLTASKS,
                             reply_markup=await gettaskskb(tasks=tasks))
    else:
        await message.answer(text=NOTASKS)


async def removetask(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()
    await removescheduler(schedid=callback.data)
    await removetaskfromdb(id=callback.data)
    await callback.message.answer(text=REMOVETASK)


async def canceltasks(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text='Action canceled.')
    await state.finish()


async def gethelp(message: Message) -> None:
    await message.answer(text=GETHELP)


async def kickbot(event: ChatMemberUpdated, state: FSMContext) -> None:
    tasks = await getusertasks(userid=event.from_user.id)
    if tasks:
        for task in tasks:
            await removescheduler(schedid=str(task.id))
            await removetaskfromdb(id=task.id)
    await state.finish()


async def geterror(update: Update, exception: BotBlocked) -> bool:
    return True

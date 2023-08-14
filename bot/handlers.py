from aiogram.types import Message, CallbackQuery, Update, ReplyKeyboardRemove, ChatMemberUpdated
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked

from bot.keyboards import getstartkb, gettimekb, gettaskskb
from bot.binancerequests import getcurrentprice
from bot.statesgroups import CoinStates
from bot.db import opendb, closedb, addtasktodb, getusertasks, removetaskfromdb
from bot.scheduler import scheduler, addscheduler, removescheduler


async def on_startup(_) -> None:
    await opendb()
    scheduler.start()


async def on_shutdown(_) -> None:
    scheduler.shutdown()
    await closedb()


async def startmes(message: Message) -> None:
    await message.answer(text='Hi!\nI am BinanceParsingBot designed to track price changes of cryptocurrency pairs'
                              ' by using BinanceAPI.\n\nFor creating new tracking task press /coin and form request '
                              'following the instructions.\n\nIf you need more information about bot and bot commands '
                              'click /help')


async def getfirstticker(message: Message) -> None:
    await message.answer(text='Send fisrt currency ticker.\n\nChoose from the 10 most popular or enter your own.'
                              '\n\nIf you want to quit press /cancel',
                         reply_markup=await getstartkb())
    await CoinStates.firstticker.set()


async def getsecondticker(message: Message, state: FSMContext) -> None:
    firstticker = message.text
    fisrttickerupper = firstticker.upper()
    async with state.proxy() as data:
        data['firstticker'] = fisrttickerupper
    await message.answer(text=f'Entered first ticker: <b>{fisrttickerupper}</b>'
                         '\n\nSend second currency ticker.'
                         '\n\nClick /cancel if first ticker is wrong.',
                         reply_markup=await getstartkb(),
                         parse_mode='HTML')
    await CoinStates.next()


async def checkcoin(message: Message, state: FSMContext) -> None:
    secondticker = message.text
    secondtickerupper = secondticker.upper()
    async with state.proxy() as data:
        data['secondticker'] = secondtickerupper
        firstticker: str = data['firstticker']
    coinprice = await getcurrentprice(firstticker=firstticker, secondticker=secondtickerupper)
    if coinprice:
        await CoinStates.next()
        await message.answer(text=f'Entered pair of cryptocurrencies: <b>{firstticker}/{secondtickerupper}</b>'
                                  f'\n\nCurrent currency ratio: <b>{coinprice}</b>''\n\nEnter tracking percentage in'
                                  ' the <b>X.XX</b> format with up to eight decimal places.\n\nIf you are not '
                                  'satisfied with the selected currency pair click /cancel',
                             reply_markup=ReplyKeyboardRemove(),
                             parse_mode='HTML')
    else:
        await message.answer(text=f'Entered pair of cryptocurrencies: {firstticker}/{secondtickerupper}.'
                             '\n\nUnfortunately BinanceAPI cant track such pair.'
                             '\n\nClick /coin to enter new currencies pair.',
                             reply_markup=ReplyKeyboardRemove(),
                             parse_mode='HTML')
        await state.finish()


async def getcoinpercent(message: Message, state: FSMContext) -> None:
    percentofchange = float(message.text)
    async with state.proxy() as data:
        data['percentofchange'] = percentofchange
    await CoinStates.next()
    await message.answer(text=f'Entered tracking percentage: <b>{message.text}%</b>'
                         '\n\nChoose tracking time.',
                         reply_markup=await gettimekb(),
                         parse_mode='HTML')


async def getcointime(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    time = int(callback.data.split('_')[1])
    checktask = await addtasktodb(state=state, callback=callback)
    if checktask == 'taskexists':
        await callback.message.answer(text='Such task already exists.'
                                      '\nClick /showalltasks to get all of your pairs or /coin to form new one')
    elif checktask == 'toomanytasks':
        await callback.message.answer(text='You\'ve reached the limit on active tasks.'
                                      '\nClick /showalltasks and delete unnecessary tasks to add a new one')
    else:
        await addscheduler(userid=callback.from_user.id, time=time, task=checktask)
        await callback.message.answer(text=f'Task added.\n\nEvery <b>{str(time)}</b> minutes the bot will send a '
                                           f'request to the API, find out the current price and send a notification '
                                           f'in case of a change by the set percentage.\n\nYou always can check your '
                                           f'current tasks by clicking /showalltasks or add new one by clicking /coin',
                                      parse_mode='HTML')
    await state.finish()


async def cancelstate(message: Message, state: FSMContext) -> None:
    await message.answer(text='Action canceled.', reply_markup=ReplyKeyboardRemove())
    await state.finish()


async def showalltasks(message: Message) -> None:
    tasks = await getusertasks(userid=message.from_user.id)
    if tasks:
        await message.answer(text='Your current pairs.\n\nClick to one of them if you want to delete it.',
                             reply_markup=await gettaskskb(tasks=tasks))
    else:
        await message.answer(text='You dont have any active tasks.\n\nClick /coin to add new one.')


async def removetask(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()
    await removescheduler(schedulerid=callback.data)
    await removetaskfromdb(id=callback.data)
    await callback.message.answer(text='Task removed.\n\nClick /coin to add new one.')


async def canceltasks(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text='Action canceled.')
    await state.finish()


async def gethelp(message: Message) -> None:
    await message.answer(text='This is a bot that informs about a change in the price of a user-selected '
                              'cryptocurrency (or several, up to 5 pieces).\n\nAfter the greeting, the user is'
                              ' prompted to enter 2 cryptocurrency tickers, or choose from the Top-10 popular ones.\n'
                              'If the API can return data for the entered pair, then the user enters the desired '
                              'percentage of change, for example 0.001%\nAfter that, the user will be prompted '
                              'to select the time period for informing.\nDepending on the selected period, a check'
                              ' will take place if the price has changed by a given percentage, the user receives a'
                              ' notification that the coin/token is growing (+0.001%) or falling (-0.001%).\nIf the '
                              'user already has subscriptions to some other cryptocurrencies, then it is possible '
                              'to call an interface with buttons where you can delete the selected pair.'
                              '\n\n/coin — create a new cryptocurrency tracking task\n/showalltasks — show a menu with'
                              ' your active task\n/cancel — exit from the form of creating tracking task')


async def kickbot(event: ChatMemberUpdated, state: FSMContext) -> None:
    userid = event.from_user.id
    tasks = await getusertasks(userid=userid)
    if tasks:
        for task in tasks:
            await removescheduler(schedulerid=str(task.id))
            await removetaskfromdb(id=str(task.id))
    else:
        pass
    await state.finish()


async def geterror(update: Update, exception: BotBlocked) -> bool:
    return True

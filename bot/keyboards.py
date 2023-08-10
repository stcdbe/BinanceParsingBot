from typing import Sequence

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from bot.dbmodels import UserTask


async def getstartkb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True,
                             row_width=3,
                             one_time_keyboard=True,
                             input_field_placeholder='Enter coin ticker')
    btn1 = KeyboardButton(text='BTC')
    btn2 = KeyboardButton(text='ETH')
    btn3 = KeyboardButton(text='XRP')
    btn4 = KeyboardButton(text='BNB')
    btn5 = KeyboardButton(text='ADA')
    btn6 = KeyboardButton(text='DOGE')
    btn7 = KeyboardButton(text='SOL')
    btn8 = KeyboardButton(text='TRX')
    btn9 = KeyboardButton(text='USDT')
    kb.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
    return kb


async def gettimekb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text='30 minutes', callback_data='time_30')
    btn2 = InlineKeyboardButton(text='1 hour', callback_data='time_60')
    btn3 = InlineKeyboardButton(text='3 hours', callback_data='time_180')
    btn4 = InlineKeyboardButton(text='6 hours', callback_data='time_360')
    btn5 = InlineKeyboardButton(text='12 hours', callback_data='time_720')
    btn6 = InlineKeyboardButton(text='Cancel', callback_data='canceltasks')
    kb.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return kb


async def gettaskskb(tasks: Sequence[UserTask]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    for task in tasks:
        kb.add(InlineKeyboardButton(text=f'{task.firstticker}/{task.secondticker} : {task.percentofchange}',
                                    callback_data=str(task.id)))
    cancelbtn = InlineKeyboardButton(text='Cancel', callback_data='canceltasks')
    kb.add(cancelbtn)
    return kb

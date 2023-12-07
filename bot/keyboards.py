from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from bot.dbmodels import Task
from bot.constants import ONE_TASK_KB


async def get_start_kb() -> ReplyKeyboardMarkup:
    tickers = ['BTC', 'ETH', 'XRP', 'BNB', 'ADA', 'DOGE', 'SOL', 'TRX', 'USDT']
    builder = ReplyKeyboardBuilder()
    for ticker in tickers:
        builder.add(KeyboardButton(text=ticker))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True,
                             one_time_keyboard=True,
                             input_field_placeholder='Enter first coin ticker')


async def get_time_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    time_and_callback = {'30 minutes': 'time_30',
                         '1 hour': 'time_60',
                         '3 hours': 'time_180',
                         '6 hours': 'time_360',
                         '12 hours': 'time_720',
                         'Cancel': 'cancel'}
    for key, val in time_and_callback.items():
        builder.add(InlineKeyboardButton(text=key, callback_data=val))
    builder.adjust(1)
    return builder.as_markup()


async def get_tasks_kb(tasks: list[Task]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for task in tasks:
        builder.add(InlineKeyboardButton(text=ONE_TASK_KB.format(tickers_pair=task.tickers_pair,
                                                                 percentage=str(task.percentage),
                                                                 interval=str(task.interval_minutes)),
                                         callback_data=str(task.id)))
    builder.add(InlineKeyboardButton(text='Cancel', callback_data='cancel'))
    builder.adjust(1)
    return builder.as_markup()

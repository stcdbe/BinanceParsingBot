from aiogram import Router, F
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import CommandStart, Command, ExceptionTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, ErrorEvent

from bot.keyboards import get_start_kb, get_time_kb, get_tasks_kb
from bot.scheduler import create_job, del_job
from bot.statesgroups import CoinPair
from bot.binancerequests import get_cur_price_api
from bot.dbservice import (get_task_db,
                           count_tasks_db,
                           create_task_db,
                           get_all_users_tasks_db,
                           del_task_db)
from bot.constants import (START_MESSAGE,
                           GET_FIRST_TICKER,
                           GET_SECOND_TICKER,
                           GET_HELP,
                           CHECK_COINS_SUCCESS,
                           CHECK_COINS_FAILED,
                           GET_PERCENTAGE,
                           TASK_EXISTS,
                           TOO_MANY_TASKS,
                           TASK_CREATED,
                           SHOW_ALL_TASKS,
                           NO_TASKS_TO_SHOW,
                           DELETE_TASK,
                           ACTION_CANCELED)


main_router = Router(name=__name__)


@main_router.message(CommandStart())
async def send_start_mes(message: Message) -> None:
    await message.answer(text=START_MESSAGE)


@main_router.message(Command('coin'))
async def get_first_ticker(message: Message, state: FSMContext) -> None:
    await state.set_state(CoinPair.first_ticker)
    await message.answer(text=GET_FIRST_TICKER, reply_markup=await get_start_kb())


@main_router.message(F.text.regexp(r'^(?![a-z]$)([A-Z]{3,5})$'), CoinPair.first_ticker)
async def get_second_ticker(message: Message, state: FSMContext) -> None:
    first_ticker = message.text.upper().strip()
    await state.update_data(first_ticker=first_ticker)
    await state.set_state(CoinPair.second_ticker)
    await message.answer(text=GET_SECOND_TICKER.format(first_ticker=first_ticker), reply_markup=await get_start_kb())


@main_router.message(F.text.regexp(r'^(?![a-z]$)([A-Z]{3,5})$'), CoinPair.second_ticker)
async def check_coins_exist(message: Message, state: FSMContext) -> None:
    second_ticker = message.text.upper()
    await state.update_data(second_ticker=second_ticker)
    coins_data = await state.get_data()
    tickers_pair = coins_data['first_ticker'] + coins_data['second_ticker']

    if coins_price := await get_cur_price_api(tickers_pair=tickers_pair):
        await state.set_state(CoinPair.percentage)
        await message.answer(text=CHECK_COINS_SUCCESS.format(first_ticker=coins_data['first_ticker'],
                                                             second_ticker=coins_data['second_ticker'],
                                                             coins_price=coins_price),
                             reply_markup=ReplyKeyboardRemove())

    else:
        await state.clear()
        await message.answer(text=CHECK_COINS_FAILED.format(first_ticker=coins_data['first_ticker'],
                                                            second_ticker=coins_data['second_ticker']),
                             reply_markup=ReplyKeyboardRemove())


@main_router.message(F.text.regexp(r'^[0-9]*[.,][0-9]{2,8}$'), CoinPair.percentage)
async def get_coin_percentage(message: Message, state: FSMContext) -> None:
    percentage = message.text
    await state.update_data(percentage=percentage)
    await message.answer(text=GET_PERCENTAGE.format(percentage=percentage), reply_markup=await get_time_kb())


@main_router.callback_query(F.data.startswith('time_'))
async def get_coin_time(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()

    task_data = await state.get_data()
    tickers_pair = task_data['first_ticker'] + task_data['second_ticker']

    if await get_task_db(user_id=callback.from_user.id, tickers_pair=tickers_pair):
        await callback.message.answer(text=TASK_EXISTS.format(tickers_pair=tickers_pair))

    elif await count_tasks_db(user_id=callback.from_user.id) >= 5:
        await callback.message.answer(text=TOO_MANY_TASKS)

    else:
        interval = int(callback.data.split('_')[1])
        task = await create_task_db(user_id=callback.from_user.id,
                                    task_data=task_data,
                                    interval=interval)
        await create_job(interval=interval,
                         job_id=str(task.id),
                         task=task)
        await callback.message.answer(text=TASK_CREATED.format(interval_time=str(task.interval_minutes),
                                                               tickers_pair=task.tickers_pair,
                                                               percentage=str(task.percentage)))

    await state.clear()


@main_router.message(Command('cancel'))
async def cancel_create_task_command(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(text=ACTION_CANCELED, reply_markup=ReplyKeyboardRemove())


@main_router.callback_query(F.data == 'cancel')
async def cancel_create_task_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(text=ACTION_CANCELED, reply_markup=ReplyKeyboardRemove())


@main_router.message(Command('showtasks'))
async def show_all_user_tasks(message: Message) -> None:
    if tasks := await get_all_users_tasks_db(user_id=message.from_user.id):
        await message.answer(text=SHOW_ALL_TASKS.format(task_count=str(len(tasks))),
                             reply_markup=await get_tasks_kb(tasks=tasks))
    else:
        await message.answer(text=NO_TASKS_TO_SHOW)


@main_router.callback_query(F.data.regexp(r'^[a-f\d]{24}$'))
async def remove_task(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()
    await del_job(job_id=callback.data)
    await del_task_db(task_id=callback.data)
    await callback.message.answer(text=DELETE_TASK)


@main_router.message(Command('help'))
async def get_help(message: Message) -> None:
    await message.answer(text=GET_HELP)


@main_router.error(ExceptionTypeFilter(TelegramForbiddenError))
async def get_blocked_bot_error(event: ErrorEvent, state: FSMContext) -> None:
    await state.clear()
    if tasks := await get_all_users_tasks_db(user_id=event.update.message.from_user.id):
        for task in tasks:
            await del_job(job_id=str(task.id))
            await del_task_db(task_id=task.id)


@main_router.error()
async def get_unknown_error(event: ErrorEvent, state: FSMContext) -> None:
    await state.clear()
    print(f'Critical error caused by {event.exception}')

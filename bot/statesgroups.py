from aiogram.fsm.state import StatesGroup, State


class CoinPair(StatesGroup):
    first_ticker = State()
    second_ticker = State()
    percentage = State()

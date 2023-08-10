from aiogram.dispatcher.filters.state import StatesGroup, State


class CoinStates(StatesGroup):
    firstticker = State()
    secondticker = State()
    percentofchange = State()

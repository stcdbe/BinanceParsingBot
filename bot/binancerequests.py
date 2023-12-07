from binance import AsyncClient
from binance.exceptions import BinanceAPIException

from bot.config import settings


async def get_cur_price_api(tickers_pair: str) -> str | None:
    client = await AsyncClient.create(api_key=settings.BINANCE_API_KEY, api_secret=settings.BINANCE_SECRET_KEY)
    try:
        result = await client.get_symbol_ticker(symbol=tickers_pair)
        price = result['price']
    except (BinanceAPIException, KeyError):
        price = None
    finally:
        await client.close_connection()
    return price

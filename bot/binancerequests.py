from binance import AsyncClient

from bot.config import BINANCEAPIKEY, BINANCESECRETKEY


async def getcurrentprice(firtick: str, sectick: str) -> str | None:
    client = await AsyncClient.create(api_key=BINANCEAPIKEY, api_secret=BINANCESECRETKEY)
    result = await client.get_symbol_ticker()
    await client.close_connection()
    for coin in result:
        if coin['symbol'] == f'{firtick}{sectick}':
            price = coin['price']
            return price

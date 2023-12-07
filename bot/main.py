import logging

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.methods import DeleteWebhook
from redis.asyncio import Redis

from bot.config import settings
from bot.dbservice import init_db
from bot.handlers import main_router
from bot.scheduler import start_scheduler, shutdown_scheduler


async def on_startup() -> None:
    await init_db()
    await start_scheduler()
    print('Starting')


async def on_shutdown() -> None:
    await shutdown_scheduler()
    print('Exited')


async def main() -> None:
    logging.basicConfig(level=logging.WARNING)

    bot = Bot(token=settings.BOT_API_TOKEN, parse_mode=ParseMode.HTML)
    aioredis = Redis.from_url(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_FSM_DB}')
    storage = RedisStorage(redis=aioredis)
    dp = Dispatcher(storage=storage)

    await bot(DeleteWebhook(drop_pending_updates=True))

    dp.startup.register(on_startup)
    dp.include_router(main_router)
    dp.shutdown.register(on_shutdown)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

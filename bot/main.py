import logging

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher.filters import Text

from bot.handlers import (startmes, getfirstticker, getsecondticker, getcoinpercent, checkcoin, getcointime,
                          cancelstate, showalltasks, canceltasks, removetask, geterror, gethelp, kickbot)
from bot.config import APITOKEN, REDISBOTDB, REDISHOST, REDISPORT
from bot.statesgroups import CoinStates
from bot.scheduler import scheduler


logging.basicConfig(level=logging.WARNING)

storage = RedisStorage2(host=REDISHOST,
                        port=REDISPORT,
                        db=REDISBOTDB,
                        pool_size=10,
                        prefix='fsm')

bot = Bot(token=APITOKEN)

dp = Dispatcher(bot=bot, storage=storage)

scheduler.ctx.add_instance(instance=bot, declared_class=Bot)

dp.register_message_handler(startmes, commands=['start'])
dp.register_message_handler(getfirstticker, commands=['coin'])
dp.register_message_handler(getsecondticker, regexp='^(?![a-z]$)([A-Z]{3,5})$', state=CoinStates.firstticker)
dp.register_message_handler(checkcoin, regexp='^(?![a-z]$)([A-Z]{3,5})$', state=CoinStates.secondticker)
dp.register_message_handler(getcoinpercent, regexp='^[0-9]*[.,][0-9]{2,8}$', state=CoinStates.percentofchange)
dp.register_callback_query_handler(getcointime, Text(startswith='time_'))
dp.register_message_handler(cancelstate, commands=['cancel'], state='*')
dp.register_message_handler(showalltasks, commands=['showalltasks'])
dp.register_callback_query_handler(removetask, regexp='^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
# dp.register_callback_query_handler(removetask, regexp='^[0-9]+$')
dp.register_callback_query_handler(canceltasks, lambda callback: callback.data == 'canceltasks', state='*')
dp.register_message_handler(gethelp, commands=['help'])
dp.register_my_chat_member_handler(kickbot, state='*')
dp.register_errors_handler(geterror, exception=BotBlocked)

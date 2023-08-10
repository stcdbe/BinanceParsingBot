import os

from dotenv import load_dotenv

load_dotenv()

APITOKEN = str(os.getenv("APITOKEN"))

BINANCEAPIKEY = str(os.getenv("BINANCEAPIKEY"))

BINANCESECRETKEY = str(os.getenv("BINANCESECRETKEY"))

PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
PGHOST = str(os.getenv("PGHOST"))
PGPORT = str(os.getenv("PGPORT"))
PGDB = str(os.getenv("PGDB"))

REDISHOST = str(os.getenv("REDISHOST"))
REDISPORT = int(os.getenv("REDISPORT"))
REDISBOTDB = int(os.getenv("REDISBOTDB"))
REDISTASKSDB = int(os.getenv("REDISTASKSDB"))

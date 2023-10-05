# BinanceParsingBot
___
### Description

Fully asynchronous Telegram bot that informs about a change in the price of a user-selected cryptocurrency (or several, up to 5 pieces).

+ After the greeting, the user is prompted to enter 2 cryptocurrency tickers, or choose from the Top-10 popular ones.
+ If the API can return data for the entered pair, then the user enters the desired percentage of change, for example 0.001%
+ After that, the user will be prompted to select the time period for informing.
+ Depending on the selected period, a check will take place if the price has changed by a given percentage, the user receives a notification that the coin/token is growing (+0.001%) or falling (-0.001%).
+ If the user already has subscriptions to some other cryptocurrencies, then it is possible to call an interface with buttons where you can delete the selected pair.

As SQL database can be used SQLite or PostgreSQL.
___
### Getting Started
#### Running on Local Machine
+ install dependencies using PIP
````
pip install -r requirements.txt 
````
+ configure environment variables in `.env` file
+ start bot in virtual environment
````
python run.py
````
#### Launch in Docker
+ configure environment variables in `.env` file
+ building the docker image
````
docker-compose build
````
+ start service
````
docker-compose up -d
````
____
#### Environment variables
| variables          | description                                   |
|:-------------------|:----------------------------------------------|
| `APITOKEN`         | Telegram bot API token                        |
| `BINANCEAPIKEY`    | Binance API key                               |
| `BINANCESECRETKEY` | Binance Secret key                            |
| `PGUSER`           | PostgreSQL user                               |
| `PGHOST`           | hostname or an IP address PostgreSQL database |
| `PGPORT`           | port from PostgreSQL database                 |
| `PGDB`             | PostgreSQL database                           |
| `PGPASSWORD`       | PostgreSQL database password                  |
| `REDISHOST`        | hostname or an IP address Redis database      |
| `REDISPORT`        | port from Redis database                      |
| `REDISBOTDB`       | Redis bot database                            |
| `REDISTASKSDB`     | Redis tasks database                          |
____
#### Tech Stack
+ `aiohttp`
+ `aiogram`
+ `python-binance`
+ `apschduler`
+ `sqlalchemy`
+ `redis` and `aioredis`
+ `docker` and `docker-compose`
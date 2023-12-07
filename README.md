# BinanceParsingBot
___
### Description

Fully asynchronous Telegram bot that informs about a change in the price of a user-selected cryptocurrency (or several, up to 5 pieces).

+ After the greeting, the user is prompted to enter 2 cryptocurrency tickers, or choose from the Top-10 popular ones.
+ If the API can return data for the entered pair, then the user enters the desired percentage of change, for example 0.001%
+ After that, the user will be prompted to select the time period for informing.
+ Depending on the selected period, a check will take place if the price has changed by a given percentage, the user receives a notification that the coin/token is growing (+0.001%) or falling (-0.001%).
+ If the user already has subscriptions to some other cryptocurrencies, then it is possible to call an interface with buttons where you can delete the selected pair.

Mongodb is used as a main database and Redis for a cache.
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
| variables            | description                     |
|:---------------------|:--------------------------------|
| `BOT_API_TOKEN`      | Telegram bot API token          |
| `BINANCE_API_KEY`    | Binance API key                 |
| `BINANCE_SECRET_KEY` | Binance Secret key              |
| `MONGO_URL`          | MongoDB URL                     |
| `MONGO_DB`           | MongoDB database                |
| `REDIS_HOST`         | hostname or an IP address Redis |
| `REDIS_PORT`         | port from Redis                 |
| `REDIS_FSM_DB`       | Redis bot database              |
| `REDIS_JOB_DB`       | Redis scheduler tasks database  |
____
#### Tech Stack
+ `aiohttp`
+ `aiogram`
+ `python-binance`
+ `apschduler`
+ `pymongo`, `motor` and `beanie`
+ `redis` and `aioredis`
+ `docker` and `docker-compose`
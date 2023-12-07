START_MESSAGE = '''Hi!
\nI am BinanceParsingBot designed to track price changes of cryptocurrency pairs by using BinanceAPI.
\nFor creating new tracking task press /coin and form request following the instructions.
\nIf you need more information about bot and bot commands click /help'''

GET_FIRST_TICKER = '''Send first currency ticker.
\nChoose from the 10 most popular or enter your own.
\nIf you want to quit press /cancel'''

GET_SECOND_TICKER = '''Entered first ticker: <b>{first_ticker}</b>
\nSend second currency ticker.
\nClick /cancel if first ticker is wrong.'''

CHECK_COINS_SUCCESS = '''Entered pair of cryptocurrencies: <b>{first_ticker}/{second_ticker}</b>
\nCurrent currency ratio: <b>{coins_price}</b>
\nEnter tracking percentage in the <b>X.XX</b> format with up to eight decimal places.
\nIf you are not satisfied with the selected currency pair click /cancel'''

CHECK_COINS_FAILED = '''Entered pair of cryptocurrencies: <b>{first_ticker}/{second_ticker}</b>.
\nUnfortunately BinanceAPI cant track such pair.
\nClick /coin to enter new currencies pair.'''

GET_PERCENTAGE = '''Entered tracking percentage: <b>{percentage}%</b>
\nChoose tracking time.'''

TASK_EXISTS = '''Task {tickers_pair} is already exists.
\nClick /showtasks to get all of your pairs or /coin to form new one'''

TOO_MANY_TASKS = '''You`ve reached the limit (5) on active tasks.
\nClick /showtasks and delete unnecessary tasks to add a new one'''

TASK_CREATED = '''Task added.
\nEvery <b>{interval_time}</b> minutes the bot will send a request to the API, find out the current price of {tickers_pair} and send a notification in case of a change by the {percentage}%.
\nYou always can check your current tasks by clicking /showtasks or add new one by clicking /coin'''

SHOW_ALL_TASKS = '''Your current pairs ({task_count}/5).
\nClick to one of them if you want to delete it.'''

ONE_TASK_KB = '''{tickers_pair} {percentage}% every {interval} minutes'''

NO_TASKS_TO_SHOW = '''You dont have any active tasks.
\nClick /coin to add new one.'''

DELETE_TASK = '''Task removed.
\nClick /coin to add new one.'''

ACTION_CANCELED = 'Action canceled'

GET_HELP = '''This is a bot that informs about a change in the price of a user-selected cryptocurrency (or several, up to 5 pieces).
\nAfter the greeting, the user is prompted to enter 2 cryptocurrency tickers, or choose from the Top-10 popular ones.
\nIf the API can return data for the entered pair, then the user enters the desired percentage of change, for example 0.001%
\nAfter that, the user will be prompted to select the time period for informing.
\nDepending on the selected period, a check will take place if the price has changed by a given percentage, the user receives a notification that the coin/token is growing (+0.001%) or falling (-0.001%).
\nIf the user already has subscriptions to some other cryptocurrencies, then it is possible to call an interface with buttons where you can delete the selected pair.
\n/coin — create a new cryptocurrency tracking task
\n/showtasks — show a menu with your active task
\n/cancel — exit from the form of creating tracking task'''

PAIR_UP = '''Pair <b>{tickers_pair}</b> rose above {percentage}%.
\nCurrent price: <b>{current_price}</b>'''

PAIR_DOWN = '''Pair <b>{tickers_pair}</b> fell below {percentage}%.
\nCurrent price: <b>{current_price}</b>'''

STARTMESSAGE = '''Hi!
\nI am BinanceParsingBot designed to track price changes of cryptocurrency pairs by using BinanceAPI.
\n\nFor creating new tracking task press /coin and form request following the instructions.
\n\nIf you need more information about bot and bot commands click /help'''

GETFIRSTTICKER = '''Send first currency ticker.
\n\nChoose from the 10 most popular or enter your own.
\n\nIf you want to quit press /cancel'''

GETSECONDTICKER = '''Entered first ticker: <b>{ticker}</b>
\n\nSend second currency ticker.
\n\nClick /cancel if first ticker is wrong.'''

CHECKCOINS = '''Entered pair of cryptocurrencies: <b>{firstticker}/{secondticker}</b>
\n\nCurrent currency ratio: <b>{coinprice}</b>
\n\nEnter tracking percentage in the <b>X.XX</b> format with up to eight decimal places.
\n\nIf you are not satisfied with the selected currency pair click /cancel'''

CHECKCOINSFAIL = '''Entered pair of cryptocurrencies: {firstticker}/{secondticker}.
\n\nUnfortunately BinanceAPI cant track such pair.
\n\nClick /coin to enter new currencies pair.'''

GETPERCENTAGE = '''Entered tracking percentage: <b>{percent}%</b>
\n\nChoose tracking time.'''

TASKEXISTS = '''Such task already exists.
\nClick /showalltasks to get all of your pairs or /coin to form new one'''

TOOMANYTASKS = '''You\'ve reached the limit on active tasks.
\nClick /showalltasks and delete unnecessary tasks to add a new one'''

TASKADDED = '''Task added.
\n\nEvery <b>{time}</b> minutes the bot will send a request to the API, find out the current price and send a notification in case of a change by the set percentage.
\n\nYou always can check your current tasks by clicking /showalltasks or add new one by clicking /coin'''

SHOWALLTASKS = '''Your current pairs.
\n\nClick to one of them if you want to delete it.'''

NOTASKS = '''You dont have any active tasks.
\n\nClick /coin to add new one.'''

REMOVETASK = '''Task removed.
\n\nClick /coin to add new one.'''

GETHELP = '''This is a bot that informs about a change in the price of a user-selected cryptocurrency (or several, up to 5 pieces).
\n\nAfter the greeting, the user is prompted to enter 2 cryptocurrency tickers, or choose from the Top-10 popular ones.
\nIf the API can return data for the entered pair, then the user enters the desired percentage of change, for example 0.001%
\nAfter that, the user will be prompted to select the time period for informing.
\nDepending on the selected period, a check will take place if the price has changed by a given percentage, the user receives a notification that the coin/token is growing (+0.001%) or falling (-0.001%).
\nIf the user already has subscriptions to some other cryptocurrencies, then it is possible to call an interface with buttons where you can delete the selected pair.
\n\n/coin — create a new cryptocurrency tracking task\n/showalltasks — show a menu with your active task
\n/cancel — exit from the form of creating tracking task'''

PAIRUP = '''Pair <b>{firstticker}/{secondticker}</b> rose above the set percentage.
\n\nCurrent price: <b>{currentprice}</b>'''

PAIRDOWN = '''Pair <b>{firstticker}/{secondticker}</b> fell below the set'percentage.
\n\nCurrent price: <b>{currentprice}</b>'''
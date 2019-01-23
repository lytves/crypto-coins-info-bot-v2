# CryptoCoinsInfoBot v2

[@CryptoCoinsInfoBot](https://t.me/CryptoCoinsInfoBot "@CryptoCoinsInfoBot") - enjoy it!

This is a simple version of a Telegram Bot, had been used [python-telegram-bot library](https://github.com/python-telegram-bot/python-telegram-bot "python-telegram-bot library Library GitHub Repository"), you can use *start_polling* or *webhook* updates methods for recieve the messages (see cryptocoinsinfobot.py code)

For use unicode emojis had been used [Emoji Library](https://github.com/carpedm20/emoji "Emoji for Python.")

APIs of [CoinMarketCap professional API](https://coinmarketcap.com/api/ "CoinMarketCap") and [CryptoCompare.com](https://www.cryptocompare.com/api/ "CryptoCompare.com") are used

**UPD 23/01/2019:** It was implemented CoinMarketCap professional API, which provide quite restricted paid plans, 
so the bot makes only 1 request/update CMC data per hour (to can be worked inside free BASIC plan), if you bought paid plan you should 
change config variable *config.TIME_INTERVAL* to get updated your data more often

---

#### Use:

For recive an actual price of some crypto coin use the keyboard with preset top crypto coins or type and send to the bot some coin name or ticker, e.g.:

> VeChain
> 
> OMG
> 
> DigixDAO


#### Settings:

Bot Settings are in the file cryptocoinsinfo/config.py:

* put your *TOKEN_BOT* and *YOUR_TELEGRAM_ALIAS* for users' feedback here.

* to can use new CoinMarketCap Professional API you should sign up on the [CoinMarketCap](https://coinmarketcap.com/api/ "CoinMarketCap")
 and put into cryptocoinsinfo/config.py your API Key to *CMC_API_KEY* variable

* bot downloads two json files with actual data from APIs (Coinmarketcap and Cryptocompare) each *TIME_INTERVAL* seconds
 and save it locally (some caching system)  

* script are using log rotations *TimedRotatingFileHandler*

---

Screenshot of the bot work:

![CryptoCoinsInfoBot](CryptoCoinsInfoBot.jpg "CryptoCoinsInfoBot")

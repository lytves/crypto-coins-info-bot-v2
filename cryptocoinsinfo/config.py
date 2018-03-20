import os

# the token of the @CryptoCoinsInfoBot
TOKEN_BOT = 'put_here'

YOUR_TELEGRAM_ALIAS = 'put_here'

TIME_INTERVAL = 150

URL_COINMARKET_SIMPLE_API = "https://api.coinmarketcap.com/v1/ticker/{}"

COINMARKET_API_URL_COINLIST = 'https://api.coinmarketcap.com/v1/ticker/?limit=0'
CRYPTOCOMPARE_API_URL_COINLIST = 'https://min-api.cryptocompare.com/data/all/coinlist'
CRYPTOCOMPARE_API_URL_PRICEMULTIFULL = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=BTC,USD'

FILE_JSON_COINMARKET = os.path.dirname(os.path.realpath(__file__)) + '/coinmarketcoins.json'
FILE_JSON_CRYPTOCOMPARE = os.path.dirname(os.path.realpath(__file__)) + '/cryptocomparecoins.json'


class JSONFiles:
    def __init__(self):
        self.coinmarketcapjson = []
        self.cryptocomparejson = {}

    def change_coinmarketcapjson(self, json1):
        assert isinstance(json1, list)
        self.coinmarketcapjson = json1
        return json1

    def change_cryptocomparejson(self, json2):
        assert isinstance(json2, dict)
        self.cryptocomparejson = json2
        return json2


# the object of class JSONFiles for save json API coins lists
jsonfiles = JSONFiles()

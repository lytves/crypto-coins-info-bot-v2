import requests
import locale
import re

from emoji import emojize

from cryptocoinsinfo.config import *
from cryptocoinsinfo.error_info_messages import *
from cryptocoinsinfo.utils import module_logger

# MACOS: 'en_GB', RASPBERRY: 'es_ES.utf8'
try:
    locale.setlocale(locale.LC_NUMERIC, 'es_ES.utf8')
except Exception as e:
    if hasattr(e, 'message'):
        ex_msg = e.message
    else:
        ex_msg = e

    module_logger.error('locale.setlocale EXCEPTION %s', ex_msg)


def parse_api_coinmarketcapjson(message_ticker):
    """
    the function to download API from the aggregators sites to local file

    :param  message_ticker: a message with a ticker from user's request
    :type   message_ticker: str

    :param  by_coin_name: to find or by coin ticket (by default) or by coin name if True
    :type   by_coin_name: Boolean
    """

    # list of all conis from coinmarketcapjson from single class "jsonfiles" of config.py
    coinmarketcapjson = jsonfiles.coinmarketcapjson

    msg_parse_api = ''

    # temporaly version: when we don't use downloaded API file, but
    # are reading coinslist from a local json file (maybe earlier downloaded manually)
    #
    # if os.path.isfile(FILE_JSON_COINMARKET):
    #     # Read configuration
    #     with open(FILE_JSON_COINMARKET) as coinmarketcapjson:
    #         try:
    #             import json
    #             coinmarketcapjson = json.load(coinmarketcapjson)
    #         except:
    #             module_logger.error('api.coinmarketcap.com! bad json file to read: %s', coinmarketcapjson)
    #             msg_parse_api += error_information()

    if not coinmarketcapjson:

        module_logger.error('api.coinmarketcap.com! Error message: there is no coinmarketcap json file')
        msg_parse_api += error_information()

        # TODO send a message to the admin (a chat, a group, a channel)

    elif coinmarketcapjson:

        # find the ticker (by name or symbol of the coin) and parsing of json file to show data
        for ticker in coinmarketcapjson['data']:

            if ticker['name'].upper() == message_ticker or \
                    ticker['symbol'].upper() == message_ticker:

                price_usd = '$?'
                rate1h = '?'
                rate1h_emoji = ''
                rate24h = '?'
                rate24h_emoji = ''
                rate7d = '?'
                rate7d_emoji = ''
                cmc_rank = '?'
                marketcap = '$?'

                # to put a header of the message
                msg_parse_api += msg_title_parse_api(str(ticker['name']), str(ticker['symbol']))

                # current price
                if ticker['quote']['USD']['price']:
                    price_usd_float = float(ticker['quote']['USD']['price'])

                    # for cut paddind zeros at the end of the price
                    if price_usd_float >= 1.0:
                        price_usd = '$' + str(locale.format("%.2f", price_usd_float, True))
                    else:
                        price_usd = '$' + str(locale.format("%.6f", price_usd_float, True)).rstrip('0')

                # 1 hour price change with emoji
                if ticker['quote']['USD']['percent_change_1h']:
                    rate1h_float = float(ticker['quote']['USD']['percent_change_1h'])
                    rate1h_emoji = parse_price_change(rate1h_float)
                    rate1h = locale.format('%.2f', rate1h_float, True)

                # 24 hours price change with emoji
                if ticker['quote']['USD']['percent_change_24h']:
                    rate24h_float = float(ticker['quote']['USD']['percent_change_24h'])
                    rate24h_emoji = parse_price_change(rate24h_float)
                    rate24h = locale.format('%.2f', rate24h_float, True)

                # 7 days price change with emoji
                if ticker['quote']['USD']['percent_change_7d']:
                    rate7d_float = float(ticker['quote']['USD']['percent_change_7d'])
                    rate7d_emoji = parse_price_change(rate7d_float)
                    rate7d = locale.format('%.2f', rate7d_float, True)

                # current cmc rank
                if ticker['cmc_rank']:
                    cmc_rank = str(ticker['cmc_rank'])

                # current market cap
                if ticker['quote']['USD']['market_cap']:
                    marketcap = str(locale.format('%.0f', float(ticker['quote']['USD']['market_cap']), True))

                msg_parse_api += '\nPrice: *' + price_usd + '*' \
                                 + '\nLast 1 hour changed: *' + rate1h + '%*' + rate1h_emoji \
                                 + '\nLast 24 hours changed: *' + rate24h + '%*' + rate24h_emoji \
                                 + '\nLast 7 days changed: *' + rate7d + '%*' + rate7d_emoji \
                                 + '\nCoinMarketCap rank: *' + cmc_rank + '*' \
                                 + '\nCoinMarketCap: *' + marketcap + '*\n'

        if msg_parse_api == '':
            msg_parse_api += error_ticker()

    else:
        module_logger.error('api.coinmarketcap.com! Error in def parse_api_coinmarketcapjson')
        msg_parse_api += error_information()

        # TODO send a message to the admin (a chat, a group, a channel)

    return '💲 *CoinMarketCap*' + msg_parse_api


def parse_api_cryptocomparejson(message_ticker):
    """
    the function to download API from the agregators sites to local file

    :param  message_ticker: a message with a ticker from user's request
    :type   message_ticker: str

    :param  by_coin_name: to find or by coin ticket (by default) or by coin name if True
    :type   by_coin_name: Boolean
    """

    # a variable cryptocomparejson from single class "jsonfiles" of config.py
    cryptocomparejson = jsonfiles.cryptocomparejson

    msg_parse_api = ''

    # temporaly version: when we don't use downloaded API file, but
    # are reading coinslist from a local json file (maybe earlier downloaded manually)
    # #
    # if os.path.isfile(FILE_JSON_CRYPTOCOMPARE):
    #     # Read configuration
    #     with open(FILE_JSON_CRYPTOCOMPARE) as cryptocomparejson:
    #         try:
    #             import json
    #             cryptocomparejson = json.load(cryptocomparejson)
    #         except:
    #             module_logger.error('min-api.cryptocompare.com! bad json file to read: %s', cryptocomparejson)
    #             msg_parse_api += error_information()
    #
    if cryptocomparejson and 'Response' in cryptocomparejson and cryptocomparejson['Response'] == 'Error':

        error = cryptocomparejson['Message']
        module_logger.error('min-api.cryptocompare.com! Error message: %s', error)
        msg_parse_api += error_information()

        # TODO send a message to the admin (a chat, a group, a channel)

    elif cryptocomparejson and 'Response' in cryptocomparejson and cryptocomparejson['Response'] == 'Success':

        # find the ticker and parsing of jsonfile for show data
        for key, value in cryptocomparejson['Data'].items():

            # if ticker_search.upper() == message_ticker:
            if key.upper() == message_ticker or value['CoinName'].upper() == message_ticker:

                # to put a header of the message
                msg_parse_api += msg_title_parse_api(str(value['CoinName']), str(value['Symbol']))

                response = requests.get(CRYPTOCOMPARE_API_URL_PRICEMULTIFULL.format(str(value['Symbol'])))

                # extract a json from response to a class 'dict'
                response_dict = response.json()

                if response.status_code == requests.codes.ok:

                    # check if APIs response is an error
                    if ('Response' in response_dict) and (response_dict['Response'] == 'Error'):
                        module_logger.error('min-api.cryptocompare.com! Error message: %s', response_dict['Message'])
                        msg_parse_api += error_ticker()

                    else:
                        ticker_raw = response_dict['RAW'][str(value['Symbol'])]
                        ticker_display = response_dict['DISPLAY'][str(value['Symbol'])]

                        price_usd = '$?'
                        price_btc = ''
                        rate24h = ''
                        rate24h_emoji = ''

                        if ticker_raw['USD']['PRICE']:
                            price_usd_float = float(ticker_raw['USD']['PRICE'])

                            # for cut paddind zeros at the end of the price
                            if price_usd_float >= 1.0:
                                price_usd = '$' + str(locale.format("%.2f", price_usd_float, True))
                            else:
                                price_usd = '$' + str(locale.format("%.6f", price_usd_float, True)).rstrip('0')

                            # for cut paddind zeros at the end of the price
                            # price_usd_float_format = "%.2f" if price_usd_float >= 1.0 else "%.6f"
                            # price_usd = '$' + str(locale.format(price_usd_float_format, price_usd_float, True)).rstrip('0').rstrip('.')

                        # current price in BTC (if the ticket is not BTC)
                        if str(value['Symbol']) != 'BTC':
                            if ticker_raw['BTC']['PRICE']:
                                price_btc = ' (' + str(
                                    locale.format('%.8f', float(ticker_raw['BTC']['PRICE']), True)) + ' BTC)'

                        # 24 hours price change with emoji
                        if ticker_display['USD']['CHANGEPCT24HOUR']:
                            rate24h_float = float(ticker_display['USD']['CHANGEPCT24HOUR'])
                            rate24h_emoji = parse_price_change(rate24h_float)
                            rate24h = locale.format('%.2f', rate24h_float, True)

                        msg_parse_api += '\nPrice: *' + price_usd + '*' + price_btc \
                                         + '\nChanged 24 hours: *' + rate24h + '%*' + rate24h_emoji + '\n'

                break

        else:
            msg_parse_api += error_ticker()

    else:
        module_logger.error('min-api.cryptocompare.com! Error in def parse_api_cryptocomparejson')
        msg_parse_api += error_information()

        # TODO send a message to the admin (a chat, a group, a channel)

    return '\n📊 *CryptoCompare*' + msg_parse_api


# compare percent and add an emoji adequate
def parse_price_change(percent):
    emoji = ''

    if percent > 20:
        emoji = emojize(' :rocket:', use_aliases=True)
    elif percent <= -20.0:
        emoji = emojize(' :sos:', use_aliases=True)
    elif percent < 0:
        emoji = emojize(' :small_red_triangle_down:', use_aliases=True)
    elif percent > 0:
        emoji = emojize(' :white_check_mark:', use_aliases=True)

    return emoji


# to add a title, info of the API parsing with name and ticker of the coin
def msg_title_parse_api(ticker_name, ticker_symbol):
    # is a strange case of token with *, which telegram markdown is provoking an error
    if ticker_symbol.find('*') >= 0:
        ticker_symbol = re.sub(r'[\*]+', '', ticker_symbol)

    # re.sub(...) is to cut all symbols
    msg_parse_api = '\nCoin Name: #' + re.sub(r'[^\S\n\t]+', '', ticker_name).strip() \
                    + '\nTicker: #' + ticker_symbol

    return msg_parse_api

import requests
import json

from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext.dispatcher import run_async

from cryptocoinsinfo.utils import command_info, message_info, text_simple, module_logger
from cryptocoinsinfo.reply_markups import *
from cryptocoinsinfo.config import *


# send a start message, command handler
@run_async
def start(update: Update, context: CallbackContext):

    command_info(update)

    usr_name = update.message.from_user.first_name
    if update.message.from_user.last_name:
        usr_name += ' ' + update.message.from_user.last_name
    usr_chat_id = update.message.chat_id

    text_response = '🇷🇺 Привет, ' + usr_name + '. Я твой Инфо Крипто Бот! Чтобы узнать цену какой-либо криптовалюты, ' \
                    ' используй клавиатуру или отправь мне *сообщение с названием или тикером* монеты/токена.' \
                    '\n\n🇬🇧 Hello, ' + usr_name + '. I am your Crypto Coins Info Bot! For receive a price of some' \
                    ' crypto use a keyboard or send me *a message with a name or a ticker* of a coin/token.'

    context.bot.send_message(usr_chat_id, text_response, parse_mode="Markdown", reply_markup=reply_markup_p1)


# bot's update error handler
@run_async
def error(update, context):
    module_logger.warning('Update caused error "%s"', context.error)

    # TODO send a message for the admin with error from here


# text messages handler for send user keyboard for all users
@run_async
def filter_text_input(update, context):

    message_info(update)

    usr_msg_text = update.message.text
    usr_chat_id = update.effective_chat.id

    # string for response
    text_response = ''

    # to work with a text request
    dict_to_request = text_simple(usr_msg_text)

    # if there is a reply_markup keyboard in a response from function - it's a menu request
    if dict_to_request['menutextresponse']:
        text_response = str(dict_to_request['menutextresponse'])

    # a simple request for a bot (coin name o coin ticket)
    elif dict_to_request['apiresponse1'] or dict_to_request['apiresponse2']:
        text_response = dict_to_request['apiresponse1'] + dict_to_request['apiresponse2']

    """
    if text_response is not empty, bot send a response to user
    """
    if text_response:
        context.bot.send_message(usr_chat_id, text_response,
                                 parse_mode="Markdown", reply_markup=dict_to_request['replymarkupresponse'])
        module_logger.info("Had send a message to a channel %s", usr_chat_id)

    else:
        module_logger.info("Don't send a message for had receive the message %s", usr_msg_text)


# a handler for download the lists of coins from API agregators by job_queue of telegram.ext
@run_async
def download_api_coinslists_handler(context):
    """
    the function to download API from the agregators sites to local file

    :param  bot: a telegram bot main object
    :type   bot: Bot

    :param  job: job.context is a name of the site-agregator, which has been send from job_queue.run_repeating... method
    :type   job: Job
    """

    job = context.job

    module_logger.info('Start a request to %s API', job.context)

    url = ''

    if job.context == 'coinmarketcap':
        url = COINMARKET_API_URL_COINLIST.format(CMC_API_KEY)
        fileoutputname = FILE_JSON_COINMARKET

    elif job.context == 'cryptocompare':
        url = CRYPTOCOMPARE_API_URL_COINLIST
        fileoutputname = FILE_JSON_CRYPTOCOMPARE

    response = requests.get(url)

    # extract a json from response to a class 'dict' or 'list'
    response_dict_list = response.json()

    if response.status_code == requests.codes.ok:

        # check if one of the APIs response is an error
        if (('status' in response_dict_list and response_dict_list['status']['error_code'] != 0) or
                (('Response' in response_dict_list) and response_dict_list['Response'] is 'Error')):

            error_msg = ''
            if job.context == 'coinmarketcap':
                error_msg = response_dict_list['status']['error_message']

            elif job.context == 'cryptocompare':
                error_msg = response_dict_list['Message']

            module_logger.error('%s error message: %s' % (job.context, error_msg))

        else:
            module_logger.info('Success download the coinslist from %s', job.context)

            with open(fileoutputname, 'w') as outfile:
                json.dump(response_dict_list, outfile)
                module_logger.info('Success save it to %s', fileoutputname)

            # save a json to variable
            if job.context == 'coinmarketcap':
                jsonfiles.update_cmc_json(response_dict_list)

            elif job.context == 'cryptocompare':
                jsonfiles.update_cc_json(response_dict_list)

    else:
        module_logger.error('%s not successfully response', job.context)

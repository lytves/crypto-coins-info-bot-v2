import os
import logging
from logging.handlers import TimedRotatingFileHandler

from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

from cryptocoinsinfo.handlers import filter_text_input, error, start, download_api_coinslists_handler, module_logger
from cryptocoinsinfo.config import TOKEN_BOT, TIME_INTERVAL

def main():
    module_logger.info("Start the @CryptoCoinsInfoBot bot!")

    # create an object "bot"
    updater = Updater(token=TOKEN_BOT)
    dispatcher = updater.dispatcher

    # bot's error handler
    dispatcher.add_error_handler(error)

    # bot's command handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # bot's text handlers
    text_update_handler = MessageHandler(Filters.text, filter_text_input)
    dispatcher.add_handler(text_update_handler)

    # here put the job for the bot
    job_queue = updater.job_queue
    job_queue.run_repeating(download_api_coinslists_handler, TIME_INTERVAL, 10, context='coinmarketcap')
    job_queue.run_repeating(download_api_coinslists_handler, TIME_INTERVAL, 40, context='cryptocompare')

    # for use start_polling() updates method
    updater.start_polling()

    # for use start_webhook updates method,
    # see https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks
    # updater.start_webhook(listen='127.0.0.1', port=5002, url_path=TOKEN_BOT)
    # updater.bot.set_webhook(url='https://0.0.0.0/' + TOKEN_BOT,
    #                   certificate=open('/etc/nginx/PUBLIC.pem', 'rb'))


if __name__ == '__main__':
    main()

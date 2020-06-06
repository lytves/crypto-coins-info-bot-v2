from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

from cryptocoinsinfo.handlers import filter_text_input, error, start, download_api_coinslists_handler
from cryptocoinsinfo.utils import module_logger
from cryptocoinsinfo.config import TOKEN_BOT, TIME_INTERVAL


def main():
    module_logger.info("Start the @CryptoCoinsInfoBot bot!")

    # create an object "bot"
    updater = Updater(token=TOKEN_BOT, use_context=True)
    dispatcher = updater.dispatcher

    # bot's error handler
    dispatcher.add_error_handler(error)

    # bot's command handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # bot's text handlers
    text_update_handler = MessageHandler(Filters.text, filter_text_input)
    dispatcher.add_handler(text_update_handler)

    #
    # *** here put the job for the bot ***
    #
    # add tasks to parse APIs from sites-aggregators to local JSON-files, is used time interval, coz
    # APIs (CMC) have pricing plans with limits
    job_queue = updater.job_queue
    job_queue.run_repeating(download_api_coinslists_handler, TIME_INTERVAL, 5, context='coinmarketcap')
    job_queue.run_repeating(download_api_coinslists_handler, TIME_INTERVAL, 10, context='cryptocompare')

    # Start the Bot start_polling() method
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.start_polling()
    updater.idle()

    # for use start_webhook updates method,
    # see https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks
    # updater.start_webhook(listen='127.0.0.1', port=5002, url_path=TOKEN_BOT)
    # updater.bot.set_webhook(url='https://0.0.0.0/' + TOKEN_BOT,
    #                   certificate=open('/etc/nginx/PUBLIC.pem', 'rb'))


if __name__ == '__main__':
    main()

# add a message with info of request problem
def error_information():
    error_text = '\n🇷🇺️ Сожалеем, нет актуальной информации. Повторите Ваш запрос позже!' \
                 '\n🇬🇧 Sorry, there is no actual information now. Please, try again later!\n'
    return error_text


# add a message if there is no ticket
def error_ticker():
    error_text = '\n🇷🇺️ Нет данных по этому тикеру' \
                 '\n🇬🇧 There is no data for this ticker\n'
    return error_text

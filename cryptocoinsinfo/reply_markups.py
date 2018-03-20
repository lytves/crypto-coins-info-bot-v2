from telegram import KeyboardButton, ReplyKeyboardMarkup

# create userkeyboard, resize = true, autohide=false
keyboard_p1 = [[KeyboardButton("Bitcoin"), KeyboardButton("Ethereum")],
            [KeyboardButton("Ripple"), KeyboardButton("Bitcoin Cash")],
            [KeyboardButton("Cardano"), KeyboardButton("page 2 ➡")]]

keyboard_p2 = [[KeyboardButton("Litecoin"), KeyboardButton("NEM")],
            [KeyboardButton("IOTA"), KeyboardButton("Dash")],
            [KeyboardButton("⬅ page 1"), KeyboardButton("page 3 ➡")]]

keyboard_p3 = [[KeyboardButton("NEO"), KeyboardButton("Monero")],
            [KeyboardButton("Stellar"), KeyboardButton("EOS")],
            [KeyboardButton("⬅ page 2"), KeyboardButton("feedback")]]

reply_markup_p1 = ReplyKeyboardMarkup(keyboard_p1, True, False)
reply_markup_p2 = ReplyKeyboardMarkup(keyboard_p2, True, False)
reply_markup_p3 = ReplyKeyboardMarkup(keyboard_p3, True, False)

import telebot
from utils import ConvertException, CurrencyConverter
from config import TOKEN, values


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def begin(message: telebot.types.Message):
    text = (f"Hello {message.chat.first_name}, I'm a currency conversion bot! To get started, enter the command"
            " in the format:\n"
            "<currency> <what we will convert into> <quantity>\n"
            "List of available currencies: /values")
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def avail_curr(message: telebot.types.Message):
    text = "Available Currencies:\n"
    for key in values.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    user_input = message.text.split(" ")
    try:
        if len(user_input) != 3:
            raise ConvertException("Missing arg")

        quote, base, amount = user_input
        result = CurrencyConverter.convert(quote, base, amount)
    except ConvertException as error:
        bot.reply_to(message, f"User fail\n{error}")
    except Exception as error:
        bot.reply_to(message, f"Fail to proceed command\n{error}")
    else:
        bot.send_message(message.chat.id, f"Price of {amount} {quote} is {result} {base}")


bot.polling()

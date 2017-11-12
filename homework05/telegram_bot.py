import telebot


access_token = "461824238:AAEFM-0gUcMe6uQwjd2wdTpYWkezqgYmD0k"
bot = telebot.TeleBot(access_token)

# @bot.message_handler(content_types=['text'])
# def echo(message):
#     bot.send_message(message.chat.id, message.text)

@bot.message_handler(commands=['tets'])
def echo(message):
    bot.send_message(message.chat.id, "alooo")

if __name__ == '__main__':
    bot.polling(none_stop=True)
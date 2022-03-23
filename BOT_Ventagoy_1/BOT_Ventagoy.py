import telebot
from extensions import APIException, Convert
from setup import TOKEN, HELP_MESS, keys

bot = telebot.TeleBot(TOKEN) # инициация бота

@bot.message_handler(commands=['start', 'help', 'values']) # блок обработки комманд
def rules(message: telebot.types.Message):
    #print(message.text)
    if (message.text) == '/help' or (message.text) == '/start':
        bot.reply_to(message, HELP_MESS)
    elif (message.text) == '/values':
        text = 'Доступные к конвертации валюты:'
        for key in keys.keys():
            text = text + (f"\n{key}--({keys[key]})") # формирование списка валют
            # print(text)
        bot.reply_to(message, text)
    else:
        bot.reply_to(message, 'Данная команда не существует')

@bot.message_handler(content_types=['text']) # обработка строки конвертации
def convert(message: telebot.types.Message):
    try:
        values = message.text.split('/')
        if len(values) != 3:
            raise APIException('Формат ввода не ссответствует требованию \
(сумма исходной валюты/исходная валюта/валюта в которую надо конвертировать)')
        amount, base, quote = values
        #bot.reply_to(message, f"{amount} {base} {quote}")
        res=Convert.get_price(amount, base, quote)
    except APIException as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        bot.send_message(message.chat.id,f'{amount} ({base}) = {res} ({quote})') # вывод результата

bot.polling(none_stop=True)

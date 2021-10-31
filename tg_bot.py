import telebot
from lacinizatar_bot import config
import requests
import re
from bs4 import BeautifulSoup
from telebot import types

token = config.BOT_TOKEN
bot = telebot.TeleBot(token)
digits_pattern = re.compile(r'^[0-9]+ [0-9]+$', re.MULTILINE)
params = {'ctext': ''}

proxy = {
    "https": 'https://45.67.59.29:3128',
    "http": 'https://45.67.59.29:3128'
}


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    try:
        print(query.query, end='!\n')
        try:
            params['ctext'] = query.query
            print(params)
            r = requests.post('https://www.zedlik.com/lacinka/pragramy/kir2lac-online/',
                              data=params)
            soup = BeautifulSoup(r.text, "html.parser")
            lacin_text = soup.find_all('div')[3].string
            print(lacin_text)
            button1 = types.InlineQueryResultArticle(id='1', title="gg",
                                           description="Результат: {!s}".format(lacin_text),
                                           input_message_content=types.InputTextMessageContent(
                                               message_text="{!s}".format(lacin_text))
                                           )
            bot.answer_inline_query(query.id, [button1], cache_time=2147483646)
        except Exception as e:
            print(e)
            pass
    except AttributeError as ex:
        return


if __name__ == '__main__':
    bot.infinity_polling()
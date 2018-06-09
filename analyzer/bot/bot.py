import telebot

from analyzer.models import DataItem
from breathum.secrets import TELEGRAM_BOT_TOKEN

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['getdataitem'])
def echo_all(message):
    try:
        uuid = message.text.split(' ')[1]
        last_data_item = DataItem.objects.filter(sensor__id=uuid).last()
        bot.reply_to(message,
                     f"Last data from sensor {uuid} is {last_data_item.data} {last_data_item.sensor.unit}")
    except Exception as e:
        bot.reply_to(message, e)

import telebot
from telebot import types

from analyzer.models import DataItem, Sensor
from breathum.secrets import TELEGRAM_BOT_TOKEN

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


# @bot.message_handler(commands=['getNearSensors'])
# def get_near_sensors(message):
#     keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#     button_geo = types.KeyboardButton(text='Отправить местоположение', request_location=True)
#     keyboard.add(button_geo)
#     bot.send_message(message.chat.id,
#                      'Для продолжения отправьте своё местоположение!',
#                      reply_markup=keyboard)

@bot.callback_query_handler(func=lambda m: m.data == 'Verify blockchain')
def verify_blockchain(m):
    response = 'Blockchain is okay' if DataItem.blockchain_verify() else 'Blockchain is broken'
    bot.reply_to(m.message, response)


@bot.callback_query_handler(func=lambda m: m.data == 'Describe sensor')
def descibe_sensor(m):
    msg = bot.send_message(m.message.chat.id, 'Введите UUID сенсора')
    bot.register_next_step_handler(msg, describe_sensor_dispatch)


def describe_sensor_dispatch(message):
    uuid = message.text
    sensor = Sensor.objects.filter(id=uuid).first()
    response = f'{sensor.title}\n' \
               f'{sensor.type}\n' \
               f'Danger Bound: {sensor.danger_bound}\n' \
               f'Risk Bound: {sensor.risk_bound}\n' \
               f'Trust Level: {sensor.trust_level}\n' \
               f'Open: {sensor.shareable}\n' \
               f'Sensor Unit: {sensor.unit}'
    bot.reply_to(message, response)


@bot.callback_query_handler(func=lambda m: m.data == 'Get available sensors')
def get_available_sensors(m):
    open_sensors = Sensor.objects.filter(shareable=True)
    response = ''
    for num, item in enumerate(open_sensors):
        response += f'{num + 1}. {item.id}\n'
    bot.reply_to(m.message, response)


@bot.callback_query_handler(func=lambda m: m.data == 'Get last DataItem')
def get_last_data_item(m):
    msg = bot.reply_to(m.message, 'Введите UUID сенсора')
    bot.register_next_step_handler(msg, get_last_data_item_dispatch)


def get_last_data_item_dispatch(message):
    uuid = message.text
    last_data_item = DataItem.objects.filter(sensor__id=uuid).last()
    bot.reply_to(message,
                 f'Last data from sensor {uuid} is {last_data_item.data} {last_data_item.sensor.unit}')


@bot.callback_query_handler(func=lambda m: m.data == 'Locate sensor')
def locate_sensor(m):
    msg = bot.reply_to(m.message, 'Введите UUID сенсора')
    bot.register_next_step_handler(msg, locate_sensor_dispatch)


def locate_sensor_dispatch(message):
    uuid = message.text
    last_data_item = DataItem.objects.filter(sensor__id=uuid).last()
    bot.send_location(message.chat.id, last_data_item.latitude, last_data_item.longitude)


@bot.message_handler(commands=['start'])
def start(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in [
            'Get last DataItem',
            'Get available sensors',
            'Describe sensor',
            'Verify blockchain',
            'Locate sensor'
        ]])
        msg = bot.send_message(message.chat.id, 'Choose one menu item:', reply_markup=keyboard)
    except Exception as e:
        bot.reply_to(message, e)

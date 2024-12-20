import telebot
from telebot import types

bot = telebot.TeleBot('7581133164:AAEiGl1U5uaGAA_mXvbHwpbGmBBMQ-GbHFk')
#LASTFM_API =

@bot.message_handler(commands=['start', 'meow', 'hello'])
def start(message):
    bot.send_message(message.chat.id, 
                     ('Приветик! Я ботик, который может найти справочную информацию о любой (нет) песне!\n'
                     'Вообщем отправь мне название песни и исполнителя вот так:\n'
                     '"Название песни - исполнитель"'), parse_mode='Markdown')
    
bot.infinity_polling()
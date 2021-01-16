# -*- coding: utf-8 -*-
import time
import configparser as cfg
import telebot
from telebot import types
from teatime import calculate_tea_cooldown_time

#token reading
def read_token(config):
    parser = cfg.ConfigParser()
    parser.read(config)
    return parser.get('creds', 'token')

token1 = read_token("config.cfg")
bot = telebot.TeleBot(token = token1)

#user data storage
class User():

    def __init__(self, chat_id, cup_radius, water_weight):
        self.chat_id = chat_id
        self.cup_radius = cup_radius
        self.water_weight = water_weight
    
    def get_id(self):
        return self.chat_id
    
    def get_radius(self):
        return self.cup_radius
    
    def update_radius(self, new_radius):
        self.cup_radius = new_radius
    
    def get_weight(self):
        return self.water_weight
    
    def update_weight(self, new_weight):
        self.water_weight = new_weight


#global var's
chat_id = None
user_params = {}
item = None
markup = None

#start message
@bot.message_handler(commands=['start','help','hello','hey'])
def welcome(message):
    #inline button
    global item
    global markup
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('Tea time', callback_data='launch')
    markup.add(item)
    bot.send_message(message.chat.id, "Welcome, {0.first_name}!\nThis bot calculates time needed for your tea, to cool down to the optimal temperature.\nPush the button to start".format(message.from_user),
    parse_mode='html', reply_markup=markup)
    
#callback
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.data == 'launch':
            bot.send_message(call.message.chat.id, "Enter teacup radius in centimetres")
            
        
    except Exception as e:
        print(repr(e))

#message send-recive
@bot.message_handler(content_types=["text"])
def get_input_from_user(message):
    global chat_id
    if float(message.text.replace(',', '.')) > 0:
        msg = float(message.text.replace(',', '.'))
        try:
            if message.chat.id not in user_params:
                user_params.update({message.chat.id : 0})
                chat_id = message.chat.id
                chat_id = User(chat_id, 0, 0)
            else:
                cup = user_params[message.chat.id]
                chat_id = User(message.chat.id, cup, 0)
            
            if chat_id.get_radius() == 0:
                msg = msg / 100
                chat_id.update_radius(msg)
                user_params.update({message.chat.id: msg})
                bot.send_message(message.chat.id, "Enter amount of water in milliliters")
                print(user_params.keys())
                print(chat_id.get_radius())
            
            else:
                cup = user_params[message.chat.id]
                chat_id = User(message.chat.id, cup, 0)
                msg = msg / 1000
                chat_id.update_weight(msg)
                resault = calculate_tea_cooldown_time(chat_id.get_radius(), chat_id.get_weight())
                bot.send_message(message.chat.id, "Tea temperature gonna be optimal in:\n{:.0f} seconds".format(resault))
                print(resault)
                chat_id.update_radius(0)
                user_params.update({message.chat.id: 0})
                #inline button
                bot.send_message(message.chat.id, 'Push the button to start',
                parse_mode='html', reply_markup=markup)

        except:
            if message.text != '/stop':
                bot.send_message(message.chat.id, "Input value error occured, try again")
                chat_id.update_radius(0)
                user_params.update({message.chat.id: 0})
                #inline button
                bot.send_message(message.chat.id, 'Push the button to start',
                parse_mode='html', reply_markup=markup)
    
    else:
        bot.send_message(message.chat.id, "Input must be a positive numeric value")

#run
if __name__ == '__main__':
     bot.polling(none_stop=True)

         
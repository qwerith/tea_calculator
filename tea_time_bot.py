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


#start message
@bot.message_handler(commands=['start'])
def welcome(message):
    #inline button
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('Tea time', callback_data='launch')

    markup.add(item)

    bot.send_message(message.chat.id, "Welcome, {0.first_name}!\nThis bot calculates time needed for your tea, to cool down to the optimal temperature.\nPush the button to start".format(message.from_user),
    parse_mode='html', reply_markup=markup)
    
count = None

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global count
    try:
        if call.data == 'launch':
            bot.send_message(call.message.chat.id, "Enter teacup radius in meters e.g 0.05 m")
            count =+ 1
            
        
    except Exception as e:
        print(repr(e))

#message send-recive
msg_list = ['test']
cup_radius = None
water_weight = None

@bot.message_handler(content_types=["text"])
def get_input_from_user(message):
    global count
    global cup_radius
    global water_weight
    if count != None:
        try:
            msg = float(message.text)
            if msg != msg_list[-1] and len(msg_list) < 2:
                msg_list.append(msg)
                try:
                    cup_radius = float(msg_list[-1])
                    if cup_radius > 0:
                        bot.send_message(message.chat.id, "Enter amount of water in kg e.g. 0.5 kg for 500 ml")
                        print('cup radius', cup_radius)
                except:
                    if message.text != '/stop':
                        bot.send_message(message.chat.id, "Input value error occured, try again")
                        del msg_list[1:]

            else:
                msg_list.append(msg)
                try:
                    if cup_radius == msg_list[-2]:
                        water_weight = float(msg_list[-1])
                        if water_weight > 0:
                            print('water weight', water_weight)
                            resault = calculate_tea_cooldown_time(cup_radius, water_weight)
                            bot.send_message(message.chat.id, "Tea temperature gonna be optimal in:\n{:.0f} seconds".format(resault))
                            print(resault)
                            del msg_list[1:]
                            count = None

                except:
                    if message.text != '/stop':
                        bot.send_message(message.chat.id, "Input value error occured, try again")
                        del msg_list[2:]      
        except:
            bot.send_message(message.chat.id, "Input value error occured, try again")
            print('Not float value')


#run
if __name__ == '__main__':
     bot.polling(none_stop=True)
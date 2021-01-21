# -*- coding: utf-8 -*-
import time
import os
import configparser as cfg
import telebot
from telebot import types
from teatime import calculate_tea_cooldown_time
from flask import Flask, request


#token reading
def read_token(config):
    parser = cfg.ConfigParser()
    parser.read(config)
    return parser.get('creds', 'token')

token1 = read_token("config.cfg")
bot = telebot.TeleBot(token=token1)
#server = Flask(__name__)


#user data storage
user_params = {}


#start message
@bot.message_handler(commands=['start','help','hello','hey'])
def welcome(message):
    if message.chat.id not in user_params:
        chat_val = {'cup_radius' : 0, 'water_weight' : 0,'switch_val' : 0, "timer_switch" : 0, "last_resault" : 0, 'preferred_temp': 50}
        user_params.update({message.chat.id : chat_val})
        print(user_params)
    #inline button
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('Tea time {}'.format('🍵'), callback_data='launch')
    markup.add(item)
    bot.send_message(message.chat.id, "Welcome, {0.first_name}!\nThis bot calculates time needed for your tea, to cool down to the optimal temperature.\nPush the button to start".format(message.from_user),
    parse_mode='html', reply_markup=markup)
    #temp choice buttons
    markup1 = types.InlineKeyboardMarkup(row_width=5)
    item_hot = types.InlineKeyboardButton('50C* {}'.format('🔥'), callback_data='50')
    item_medium = types.InlineKeyboardButton('36C* {}'.format('👌'), callback_data='36.6')
    item_cold = types.InlineKeyboardButton('20C* {}'.format('❄️'), callback_data='20')
    markup1.add(item_hot, item_medium, item_cold)
    bot.send_message(message.chat.id, 'Choose your desired tea temperature, default is 50C*\nYou can use "/temp" to set desired temperature.',
    parse_mode='html', reply_markup=markup1)
    
#temperature setting handler
@bot.message_handler(commands=['temp'])
def temp_command(message):
    if message.chat.id in user_params:
        markup1 = types.InlineKeyboardMarkup(row_width=5)
        item_hot = types.InlineKeyboardButton('50C* {}'.format('🔥'), callback_data='50')
        item_medium = types.InlineKeyboardButton('36C* {}'.format('👌'), callback_data='36.6')
        item_cold = types.InlineKeyboardButton('20C* {}'.format('❄️'), callback_data='20')
        markup1.add(item_hot, item_medium, item_cold)
        bot.send_message(message.chat.id, 'Choose your desired tea temperature\nYour current chosen temperature is {}C*'.format(user_params[message.chat.id]['preferred_temp']),
        parse_mode='html', reply_markup=markup1)
    else:
        chat_val = {'cup_radius' : 0, 'water_weight' : 0,'switch_val' : 0, "timer_switch" : 0, "last_resault" : 0, 'preferred_temp': 50}
        user_params.update({message.chat.id : chat_val})
        print(user_params)
        markup1 = types.InlineKeyboardMarkup(row_width=5)
        item_hot = types.InlineKeyboardButton('50C* {}'.format('🔥'), callback_data='50')
        item_medium = types.InlineKeyboardButton('36C* {}'.format('👌'), callback_data='36.6')
        item_cold = types.InlineKeyboardButton('20C* {}'.format('❄️'), callback_data='20')
        markup1.add(item_hot, item_medium, item_cold)
        bot.send_message(message.chat.id, 'Choose your desired tea temperature\nYour current chosen temperature is {}C*'.format(user_params[message.chat.id]['preferred_temp']),
        parse_mode='html', reply_markup=markup1)



#web
#@server.route('/' + token1, methods=['POST'])
#def getMessage():
    #bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    #return "!", 200


#@server.route("/")
#def webhook():
    #bot.remove_webhook()
    #bot.set_webhook(url='https://tea-bot-tg.herokuapp.com/' + token1)
    #return "!", 200

#callback
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    temp_list = ['50','36.6','20']
    try:
        if call.data in temp_list and call.message.chat.id not in user_params:
            chat_val = {'cup_radius': 0, 'water_weight': 0, 'switch_val': 1, "timer_switch": 0, "last_resault": 0, 'preferred_temp': 50}
            user_params.update({call.message.chat.id: chat_val})
            user_params[call.message.chat.id].update({'preferred_temp': float(call.data)})
            print('new desired temp for:', call.message.chat.id, 'is', call.data)
            markup = types.InlineKeyboardMarkup(row_width=5)
            item = types.InlineKeyboardButton('Tea time {}'.format('🍵'), callback_data='launch')
            markup.add(item)
            bot.send_message(call.message.chat.id, 'Desired tea temperature is set to {}C*'.format(user_params[call.message.chat.id]['preferred_temp']),
            parse_mode='html', reply_markup=markup)
        elif call.data in temp_list and call.message.chat.id in user_params:
            user_params[call.message.chat.id].update({'preferred_temp': float(call.data)})
            print('new desired temp for:', call.message.chat.id, 'is', call.data)
            markup = types.InlineKeyboardMarkup(row_width=5)
            item = types.InlineKeyboardButton('Tea time {}'.format('🍵'), callback_data='launch')
            markup.add(item)
            bot.send_message(call.message.chat.id, 'Desired tea temperature is set to {}C*'.format(user_params[call.message.chat.id]['preferred_temp']),
            parse_mode='html', reply_markup=markup)
 
    except Exception as e:
        print(repr(e))

    try:
        if call.data == 'launch' and call.message.chat.id not in user_params:
            chat_val = {'cup_radius' : 0, 'water_weight' : 0,'switch_val' : 1, "timer_switch" : 0, "last_resault" : 0,'preferred_temp': 50}
            user_params.update({call.message.chat.id: chat_val})
            bot.send_message(call.message.chat.id, "Enter teacup radius in centimetres")
            print(user_params)
        elif call.data == 'launch':
            if user_params[call.message.chat.id]["timer_switch"] == 1:
                bot.send_message(call.message.chat.id, "The tea timer will be reset if you proceed")
            bot.send_message(call.message.chat.id, "Enter teacup radius in centimetres")
            user_params[call.message.chat.id].update({'switch_val':1})
            print(user_params)
        
    except Exception as e:
        print(repr(e))


#message send-recive
@bot.message_handler(content_types=["text"])
def get_input_from_user(message):
    if message.chat.id in user_params and user_params[message.chat.id]['switch_val'] == 1:
        try:
            if float(message.text.replace(',', '.')) > 0:
                msg = float(message.text.replace(',', '.'))   
            else:
                bot.send_message(message.chat.id, "Input must be a positive numeric value")
        
        except ValueError:
            print('value error')
        
        try:
            chat_id = message.chat.id
            if user_params[chat_id]['cup_radius'] == 0:
                msg = msg / 100
                user_params[chat_id].update({'cup_radius' : msg})
                bot.send_message(message.chat.id, "Enter amount of water in milliliters")
                print(user_params.keys())
                print(user_params[chat_id]['cup_radius'])
            
            else:
                #timer_switch
                if user_params[message.chat.id]["last_resault"] != 0 and user_params[chat_id]['timer_switch'] != 0:
                    user_params[message.chat.id].update({"timer_switch": 0})
                else:
                    user_params[message.chat.id].update({"timer_switch": 1})
                ###
                #resault_calculation
                msg = msg / 1000
                user_params[chat_id].update({'water_weight': msg})
                resault = calculate_tea_cooldown_time(user_params[chat_id]['cup_radius'], user_params[chat_id]['water_weight'], user_params[chat_id]['preferred_temp'])
                print(resault)
                m, s = divmod(resault, 60)
                print(resault / 60)
                if resault >= 60:
                    bot.send_message(message.chat.id, "You will receive notification in:\n{:.0f} minutes and {:.0f} seconds".format(m, s))

                else:
                    bot.send_message(message.chat.id, "You will receive notification in:\n{:.0f} seconds".format(resault))
                #switch values to stock
                user_params[chat_id].update({'cup_radius' : 0})
                user_params[chat_id].update({'water_weight': 0})
                user_params[chat_id].update({'switch_val': 0})
                #inline button
                markup = types.InlineKeyboardMarkup(row_width=2)
                item = types.InlineKeyboardButton('Tea time {}'.format('🍵'), callback_data='launch')
                markup.add(item)
                bot.send_message(message.chat.id, 'Push the button to start',
                parse_mode='html', reply_markup=markup)
                #timer
                user_params[chat_id].update({'last_resault': resault})
                if user_params[message.chat.id]['timer_switch'] == 1:
                    print('timer one started')
                    send = True
                    for i in range(int(resault)):
                        time.sleep(1)
                        if user_params[chat_id]['timer_switch'] != 1:
                            print('timer one has been stoped')
                            send = False
                            break
                    if send == True:
                        bot.send_message(message.chat.id, 'Your tea is ready sir!')
                        user_params[chat_id].update({'timer_switch': 0})
                        user_params[chat_id].update({'last_resault': 0})
                else:
                    send1 = True
                    print('timer two started')
                    for i in range(int(resault)):
                        time.sleep(1)
                        if user_params[chat_id]['timer_switch'] == 1:
                            print('timer two stoped')
                            send1 = False
                            break
                    if send1 == True:
                        bot.send_message(message.chat.id, 'Your tea is ready sir!')
                        user_params[chat_id].update({'timer_switch': 0})
                        user_params[chat_id].update({'last_resault': 0})
                        

        except:
            if message.text != '/stop':
                bot.send_message(message.chat.id, "Input value error occured, try again")
                print('error marker')
                #switch values to stock
                user_params[chat_id].update({'cup_radius' : 0})
                user_params[chat_id].update({'water_weight': 0})
                user_params[chat_id].update({'switch_val': 0})
                user_params[chat_id].update({"timer_switch": 0})
                user_params[chat_id].update({"last_resault": 0})
                #inline button
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton('Tea time {}'.format('🍵'), callback_data='launch')
                markup.add(item1)
                bot.send_message(message.chat.id, 'Push the button to start',
                parse_mode='html', reply_markup=markup)
    else:
        print('error marker1')


#run
if __name__ == '__main__':
    bot.polling(none_stop=True)

         
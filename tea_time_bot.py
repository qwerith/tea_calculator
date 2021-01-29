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
@bot.message_handler(commands=['start','hello','hey','hi'])
def welcome(message):
    if message.chat.id not in user_params:
        chat_val = {'cup_radius' : 0, 'water_weight' : 0,'switch_val' : 0, "timer_switch" : 0, "last_resault" : 0, 'preferred_temp': 50, 'saved cup_radius' : 0, 'saved water_weight' : 0}
        user_params.update({message.chat.id : chat_val})
        print(user_params)
    #inline button
    markup = inline_buttons('launch', message.chat.id)
    bot.send_message(message.chat.id, "Welcome,{0.first_name}!\nThis bot calculates time needed for your tea, to cool down to the optimal temperature. Push the button to start".format(message.from_user), 
    parse_mode='html', reply_markup=markup)
    
    
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "This bot calculates time needed for your tea, to cool down to the optimal temperature.\nHere is list of commands you may wanna use\n'/start'- to launch bot\n'/temp'- to set desired temperatue\n'/mycup'- to start timer for your saved cup\n'/del' - to delete your saved cup")

@bot.message_handler(commands=['temp'])
def temp(message):
    if message.chat.id not in user_params:
        chat_val = {'cup_radius' : 0, 'water_weight' : 0,'switch_val' : 0, "timer_switch" : 0, "last_resault" : 0, 'preferred_temp': 50, 'saved cup_radius' : 0, 'saved water_weight' : 0}
        user_params.update({message.chat.id : chat_val})
        print(user_params)
    inline_buttons('temp_choice', message.chat.id)

@bot.message_handler(commands=['mycup'])
def mycup(message):
    if message.chat.id not in user_params:
        chat_val = {'cup_radius' : 0, 'water_weight' : 0,'switch_val' : 0, "timer_switch" : 0, "last_resault" : 0, 'preferred_temp': 50, 'saved cup_radius' : 0, 'saved water_weight' : 0}
        user_params.update({message.chat.id : chat_val})
        print(user_params)
    if user_params[message.chat.id]['saved cup_radius'] == 0 or user_params[message.chat.id]['saved water_weight'] == 0:
        bot.send_message(message.chat.id, 'No saved cup found')
    markup = inline_buttons('mycup', message.chat.id)
    bot.send_message(message.chat.id, 'Proceed to save parameters',
    parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['del'])
def delete(message):
    if message.chat.id not in user_params:
        chat_val = {'cup_radius' : 0, 'water_weight' : 0,'switch_val' : 0, "timer_switch" : 0, "last_resault" : 0, 'preferred_temp': 50, 'saved cup_radius' : 0, 'saved water_weight' : 0}
        user_params.update({message.chat.id : chat_val})
        print(user_params)
        bot.send_message(message.chat.id, 'No saved cup found')
    elif user_params[message.chat.id]['saved cup_radius'] == 0 or user_params[message.chat.id]['saved water_weight'] == 0:
        bot.send_message(message.chat.id, 'No saved cup found')
    elif user_params[message.chat.id]['saved cup_radius'] != 0 and user_params[message.chat.id]['saved water_weight'] != 0:
        inline_buttons('delete', message.chat.id)


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


#inline buttons
def inline_buttons(button, message_id):
    if button == 'temp_choice':
        markup = types.InlineKeyboardMarkup(row_width=4)
        item_hot = types.InlineKeyboardButton('50C* {}'.format('🔥'), callback_data='50')
        item_medium = types.InlineKeyboardButton('36C* {}'.format('👌'), callback_data='36.6')
        item_cold = types.InlineKeyboardButton('20C* {}'.format('❄️'), callback_data='20')
        markup.add(item_hot, item_medium, item_cold)
        bot.send_message(message_id, 'Choose your desired tea temperature\nYour current chosen temperature is {}C*'.format(user_params[message_id]['preferred_temp']),
        parse_mode='html', reply_markup=markup)
        return(markup)
    elif button == 'launch':
        markup = types.InlineKeyboardMarkup(row_width=2)
        item = types.InlineKeyboardButton('Tea time {}'.format('🍵'), callback_data='launch')
        markup.add(item)
        return (markup)
    elif button == 'save':
        markup = types.InlineKeyboardMarkup(row_width=2)
        item = types.InlineKeyboardButton('Yes', callback_data='yes')
        item1 = types.InlineKeyboardButton('No', callback_data='no')
        markup.add(item, item1)
        if user_params[message_id]['saved cup_radius'] == 0 or user_params[message_id]['saved water_weight'] == 0:
            bot.send_message(message_id, 'Do you want to save this cup profile?', parse_mode='html', reply_markup=markup)
        else:
            bot.send_message(message_id, 'Do you want to rewrite your saved this cup profile? ({:.0f}sm, {:.0f}ml)'.format(user_params[message_id]['saved cup_radius'] * 100, user_params[message_id]['saved water_weight'] * 1000),
            parse_mode='html', reply_markup=markup)
        return (markup)
    elif button == 'mycup':
        markup = types.InlineKeyboardMarkup(row_width=2)
        item = types.InlineKeyboardButton('My cup {}'.format('☕'), callback_data='mycup')
        markup.add(item)
        return (markup)
    elif button == 'delete':
        markup = types.InlineKeyboardMarkup(row_width=2)
        item = types.InlineKeyboardButton('Yes', callback_data='yes_delete')
        item1 = types.InlineKeyboardButton('No', callback_data='no_delete')
        markup.add(item, item1)
        bot.send_message(message_id, 'Do you want to delete your cup profile?', parse_mode='html', reply_markup=markup)
        return (markup)

#input check
def input_check(message_text, message_id):
    if float(message_text.replace(',', '.')) > 0:
        msg = float(message_text.replace(',', '.'))
    else:
        bot.send_message(message_id, "Input must be a positive numeric value")       
    return(msg)

#input check1
def input_check1(message_id, msg):
    msg = msg / 100
    user_params[message_id].update({'cup_radius' : msg})
    bot.send_message(message_id, "Enter amount of water in milliliters")
    print(user_params.keys())
    print(user_params[message_id]['cup_radius'])
    return(msg)

#resault_calculation
def resault_calculation(cup_radius, water_weight, preferred_temp, message_id):
    resault = calculate_tea_cooldown_time(cup_radius, water_weight, preferred_temp)
    print(resault)
    m, s = divmod(resault, 60)
    print(resault / 60)
    if resault >= 60 and cup_radius == user_params[message_id]['saved cup_radius'] and water_weight == user_params[message_id]['saved water_weight']:
        markup = inline_buttons('mycup', message_id)
        bot.send_message(message_id, "You will receive notification in:\n{:.0f} minutes and {:.0f} seconds".format(m, s), parse_mode='html', reply_markup=markup)               
    elif cup_radius == user_params[message_id]['saved cup_radius'] and water_weight == user_params[message_id]['saved water_weight']:
            markup = inline_buttons('mycup', message_id)
            bot.send_message(message_id, "You will receive notification in:\n{:.0f} seconds".format(resault), parse_mode='html', reply_markup=markup)      
    if resault >= 60:
        bot.send_message(message_id, "You will receive notification in:\n{:.0f} minutes and {:.0f} seconds".format(m, s))       
    else:
         bot.send_message(message_id, "You will receive notification in:\n{:.0f} seconds".format(resault))
    if cup_radius != user_params[message_id]['saved cup_radius'] or water_weight != user_params[message_id]['saved water_weight']:
        inline_buttons('save', message_id)
    return(resault)

#timer switch
def timer_switch(message_id):
    if user_params[message_id]["last_resault"] != 0 and user_params[message_id]['timer_switch'] != 0:
        user_params[message_id].update({"timer_switch": 0})
    else:
        user_params[message_id].update({"timer_switch": 1})
    return()

#timer
def timer(message_id, resault):
    user_params[message_id].update({'last_resault': resault})
    if user_params[message_id]['timer_switch'] == 1:
        print('timer one started')
        send = True
        for i in range(int(resault)):
            time.sleep(1)
            if user_params[message_id]['timer_switch'] != 1:
                print('timer one has been stoped')
                send = False
                break
        if send == True:
            bot.send_message(message_id, 'Your tea is ready sir!')
            user_params[message_id].update({'timer_switch': 0})
            user_params[message_id].update({'last_resault': 0})
    else:
        send1 = True
        print('timer two started')
        for i in range(int(resault)):
            time.sleep(1)
            if user_params[message_id]['timer_switch'] == 1:
                print('timer two has been stoped')
                send1 = False
                break
        if send1 == True:
            bot.send_message(message_id, 'Your tea is ready sir!')
            user_params[message_id].update({'timer_switch': 0})
            user_params[message_id].update({'last_resault': 0})

#callback
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    temp_list = ['50', '36.6', '20']
    call_back_list = ['yes','no']
    try:
        if call.data in call_back_list and call.message.chat.id not in user_params:
            call.data = 'launch'    
        elif call.data == 'yes' and user_params[call.message.chat.id]['cup_radius'] != 0 and user_params[call.message.chat.id]['water_weight'] != 0:
            user_params[call.message.chat.id].update({'saved cup_radius': user_params[call.message.chat.id]['cup_radius']})
            user_params[call.message.chat.id].update({'saved water_weight': user_params[call.message.chat.id]['water_weight']})
            #switch values to stock
            user_params[call.message.chat.id].update({'cup_radius' : 0})
            user_params[call.message.chat.id].update({'water_weight': 0})
            markup = inline_buttons('mycup', call.message.chat.id)
            bot.send_message(call.message.chat.id, "Your cup has been saved", parse_mode='html', reply_markup=markup)
            print('saved data:', user_params[call.message.chat.id]['saved cup_radius'], user_params[call.message.chat.id]['saved water_weight'])
        elif call.data == 'no':
            user_params[call.message.chat.id].update({'cup_radius' : 0})
            user_params[call.message.chat.id].update({'water_weight': 0})
            #inline button
            markup = inline_buttons('launch', call.message.chat.id)
            bot.send_message(call.message.chat.id, 'Push the button to start', parse_mode='html', reply_markup=markup)
        elif call.data == 'mycup' and call.message.chat.id not in user_params or user_params[call.message.chat.id]['saved cup_radius'] == 0 or user_params[call.message.chat.id]['saved water_weight'] == 0:
            call.data = 'launch'
        elif call.data == 'mycup':
            timer_switch(call.message.chat.id)
            resault = resault_calculation(user_params[call.message.chat.id]['saved cup_radius'], user_params[call.message.chat.id]['saved water_weight'], user_params[call.message.chat.id]['preferred_temp'], call.message.chat.id)
            print(user_params)
            timer(call.message.chat.id, resault)
        elif call.data == 'yes_delete':
            user_params[call.message.chat.id].update({'saved cup_radius': 0 })
            user_params[call.message.chat.id].update({'saved water_weight': 0})
            bot.send_message(call.message.chat.id, 'Cup profile has been deleted')
        elif call.data == 'no_delete':
            markup = inline_buttons('launch', call.message.chat.id)
            bot.send_message(call.message.chat.id, 'Push the button to start',
            parse_mode='html', reply_markup=markup)
            
    except Exception as e:
        print(repr(e))

    try:
        if call.data == 'launch' and call.message.chat.id not in user_params:
            chat_val = {'cup_radius' : 0, 'water_weight' : 0,'switch_val' : 1, "timer_switch" : 0, "last_resault" : 0,'preferred_temp': 50, 'saved cup_radius' : 0, 'saved water_weight' : 0}
            user_params.update({call.message.chat.id: chat_val})
            markup = inline_buttons('temp_choice', call.message.chat.id)
            bot.send_message(call.message.chat.id, "Enter teacup radius in centimetres")
            print(user_params)
        elif call.data == 'launch':
            user_params[call.message.chat.id].update({'cup_radius' : 0})
            user_params[call.message.chat.id].update({'water_weight': 0})
            markup = inline_buttons('temp_choice', call.message.chat.id)
            if user_params[call.message.chat.id]["timer_switch"] == 1:
                bot.send_message(call.message.chat.id, "The tea timer will be reset if you proceed")
            bot.send_message(call.message.chat.id, "Enter teacup radius in centimetres")
            user_params[call.message.chat.id].update({'switch_val': 1})
            print(user_params)

    except Exception as e:
        print(repr(e))

    try:
        if call.data in temp_list and call.message.chat.id not in user_params:
            chat_val = {'cup_radius': 0, 'water_weight': 0, 'switch_val': 1, "timer_switch": 0, "last_resault": 0, 'preferred_temp': 50}
            user_params.update({call.message.chat.id: chat_val})
            user_params[call.message.chat.id].update({'preferred_temp': float(call.data)})
            print('new desired temp for:', call.message.chat.id, 'is', call.data)
            markup = inline_buttons('launch', call.message.chat.id)
            bot.send_message(call.message.chat.id, 'Desired tea temperature is set to {}C*'.format(user_params[call.message.chat.id]['preferred_temp']),
            parse_mode='html', reply_markup=markup)
        elif call.data in temp_list and call.message.chat.id in user_params:
            user_params[call.message.chat.id].update({'preferred_temp': float(call.data)})
            print('new desired temp for:', call.message.chat.id, 'is', call.data)
            bot.send_message(call.message.chat.id, 'Desired tea temperature is set to {}C*'.format(user_params[call.message.chat.id]['preferred_temp']),
            parse_mode='html')
 
    except Exception as e:
        print(repr(e))
    

#message send-recive
@bot.message_handler(content_types=["text"])
def get_input_from_user(message):
    if message.chat.id in user_params and user_params[message.chat.id]['switch_val'] == 1:
        try:
            chat_id = message.chat.id
            msg = input_check(message.text, message.chat.id)
            if user_params[chat_id]['cup_radius'] == 0:
                input_check1(message.chat.id, msg)
            else:
                #timer_switch
                timer_switch(chat_id)
                #resault_calculation
                msg = msg / 1000
                user_params[message.chat.id].update({'water_weight': msg})
                resault = resault_calculation(user_params[chat_id]['cup_radius'], user_params[chat_id]['water_weight'], user_params[chat_id]['preferred_temp'], message.chat.id)
                user_params[message.chat.id].update({'switch_val': 0})
                #timer
                timer(message.chat.id, resault)
        
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
                markup = inline_buttons('launch', message.chat.id)
                bot.send_message(message.chat.id, 'Push the button to start',
                parse_mode='html', reply_markup=markup)
                
    else:
        print('error, input switch off')

#run
if __name__ == '__main__':
     bot.polling(none_stop=True)
    #server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
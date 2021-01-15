# -*- coding: utf-8 -*-
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
user_params = {}


#start message
@bot.message_handler(commands=['start','help','hello','hey'])
def welcome(message):
    if message.chat.id not in user_params:
        chat_val = {'cup_radius' : 0, 'water_weight' : 0,'switch_val' : 0}
        user_params.update({message.chat.id : chat_val})
        print(user_params)
    
    #inline button
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('Tea time {}'.format('🍵'), callback_data='launch')
    markup.add(item)
    bot.send_message(message.chat.id, "Welcome, {0.first_name}!\nThis bot calculates time needed for your tea, to cool down to the optimal temperature.\nPush the button to start".format(message.from_user),
    parse_mode='html', reply_markup=markup)
    
#callback
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.data == 'launch':
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
                msg = msg / 1000
                user_params[chat_id].update({'water_weight' : msg})
                resault = calculate_tea_cooldown_time(user_params[chat_id]['cup_radius'], user_params[chat_id]['water_weight'])
                print(resault)
                m, s = divmod(resault, 60)
                print(resault / 60)
                if resault >= 60:
                    bot.send_message(message.chat.id, "Tea temperature gonna be optimal in:\n minutes {:.0f} and {:.0f} seconds".format(m, s))

                else:
                    bot.send_message(message.chat.id, "Tea temperature gonna be optimal in:\n {:.0f} seconds".format(resault))
                #switch values to stock
                user_params[chat_id].update({'cup_radius' : 0})
                user_params[chat_id].update({'water_weight': 0})
                user_params[chat_id].update({'switch_val' : 0})
                #inline button
                markup = types.InlineKeyboardMarkup(row_width=2)
                item = types.InlineKeyboardButton('Tea time {}'.format('🍵'), callback_data='launch')
                markup.add(item)
                bot.send_message(message.chat.id, 'Push the button to start',
                parse_mode='html', reply_markup=markup)

        except:
            if message.text != '/stop':
                bot.send_message(message.chat.id, "Input value error occured, try again")
                print('error marker')
                #switch values to stock
                user_params[chat_id].update({'cup_radius' : 0})
                user_params[chat_id].update({'water_weight': 0})
                user_params[chat_id].update({'switch_val' : 0})
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

         
import sys
import os

dir_of_executable = os.path.dirname(__file__)
path_to_project_root = os.path.abspath(os.path.join(dir_of_executable, '..'))
sys.path.insert(0, path_to_project_root)
os.chdir(path_to_project_root)

from core.service.RouterAuthService import RouterAuthService

from core.actions.ChangePassword import *
from core.actions.Reboot import *
from core.actions.EnableWhitelist import *

import telebot
import configparser

from telebot import types

bot_config = configparser.ConfigParser()
bot_config.read('config/telegram.ini')

bot = telebot.TeleBot(bot_config['Authentication']['token'])

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    router_restart = types.KeyboardButton('Перезагрузка')
    router_changePassword = types.KeyboardButton('Изменить пароль')
    router_enableWhitelist = types.KeyboardButton('Включить/выключить белый список')
    
    markup.add(router_restart, router_changePassword, router_enableWhitelist)
    
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!'.format(message.from_user), reply_markup = markup)
    

router_config = configparser.ConfigParser()
router_config.read('config/router.ini')

@bot.message_handler(content_types=['text'])
def bot_message(message):
    router = RouterAuthService()
    try:
        authInfo = router.auth(router_config['Authentication']['login'], 
                    router_config['Authentication']['password'])
    except HttpRequestException as exception:
        print(exception.message)
        print(f'Status code: {str(exception.status_code)}')
        if(exception.status_code == 200):
            print(exception.response)
            
    if message.chat.type == 'private':
        if message.text=='Перезагрузка':
            reboot(authInfo)
    try:       
        router.logout()
    except HttpRequestException as exception:
        print(exception.message)
        print(f'Status code: {str(exception.status_code)}')
        if(exception.status_code == 200):
            print(exception.response)
            
bot.polling(none_stop = True)
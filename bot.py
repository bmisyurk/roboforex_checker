# coding=utf-8
import time
import json
import os
import re
import sqlite3
import requests
import threading

from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
from telebot import apihelper, types, TeleBot

TRAIN_DATA = {}


with open('credentials_for_bot.json', 'r', encoding='utf-8') as bot_file, \
        open('config.json', 'r', encoding='utf-8') as config_file:
    credentials_bot = json.load(bot_file)
    config_file = json.load(config_file)

bot = TeleBot(credentials_bot["telegram"]["roboforex_bot"], skip_pending=True)


@bot.message_handler(commands=['log'])
def send_log(message):
    if message.chat.id == 368246133:
        try:
            with open(f"logs/{datetime.now().strftime('%Y-%m-%d')}.txt", 'r', encoding='utf-8') as log_file:
                bot.send_document(message.chat.id, log_file)
        except:
            bot.send_document(message.chat.id, 'File not exist for date today')


@bot.message_handler(commands=['interval'])
def change_interval(message):
    try:
        config_file["interval"] = int(message.text.split(' ')[1])
        with open('config.json', 'w') as f:
            json.dump(config_file, f, indent=2)
        bot.send_message(message.chat.id,
                         f'New interval is {config_file["interval"]}')
    except Exception as e:
        bot.send_message(credentials_bot["telegram"]["user_bmi"], text=f'Error bot.py(interval): {e}')


@bot.message_handler(commands=['percent'])
def change_percent(message):
    try:
        inputs = message.text.split(' ')
        config_file[inputs[1]]["percent"] = int(inputs[2])
        with open('config.json', 'w') as f:
            json.dump(config_file, f, indent=2)
        bot.send_message(message.chat.id,
                         f'Percent {inputs[2]} is changed for account {inputs[1]}')
    except Exception as e:
        bot.send_message(credentials_bot["telegram"]["user_bmi"], text=f'Error bot.py(percent): {e}')


@bot.message_handler(commands=['on'])
def change_interval(message):
    try:
        config_file["active"] = True
        with open('config.json', 'w') as f:
            json.dump(config_file, f, indent=2)
        bot.send_message(message.chat.id, f'Monitoring successfully enabled')
    except Exception as e:
        bot.send_message(credentials_bot["telegram"]["user_bmi"], text=f'Error bot.py(active on): {e}')


@bot.message_handler(commands=['off'])
def change_interval(message):
    try:
        config_file["active"] = False
        with open('config.json', 'w') as f:
            json.dump(config_file, f, indent=2)
        bot.send_message(message.chat.id, f'Monitoring successfully disabled')
    except Exception as e:
        bot.send_message(credentials_bot["telegram"]["user_bmi"], text=f'Error bot.py(active off): {e}')


@bot.message_handler(commands=['file'])
def send_file(message):
    if message.chat.id == 368246133:
        with open('config.json', 'r', encoding='utf-8') as log_file:
            bot.send_document(message.chat.id, log_file)


bot.polling(none_stop=True)

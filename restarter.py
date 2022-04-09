# coding=utf-8
import os
import json
import time
import subprocess
from telebot import apihelper, types, TeleBot

with open('credentials_for_bot.json', 'r', encoding='utf-8') as bot_file:
    credentials_bot = json.load(bot_file)

bot = TeleBot(credentials_bot["telegram_restarter"]["api_token"], skip_pending=True)


@bot.message_handler(commands=['restart_ban'])
def restart(message):
    comm = ['SCHTASKS', '/End', '/TN', '\\bmi\\ban_bmi']
    subprocess.run(comm)
    comm = ['SCHTASKS', '/Run', '/TN', '\\bmi\\ban_bmi']
    subprocess.run(comm)
    os.system("TASKKILL /F /IM chromedriver.exe /T")
    os.system("TASKKILL /F /IM chrome.exe /T")
    if message.chat.id != 368246133:
        bot.send_message(message.chat.id, 'Bot restarted')
    bot.send_message(368246133, 'Bot restarted')


@bot.message_handler(commands=['restart_uz'])
def restart(message):
    # with open('C:\\bmi\\gd\\current_id.txt', 'r', encoding='utf-8') as current_id_file:
    #     pid_id = int(current_id_file.readline())
    comm = ['SCHTASKS', '/End', '/TN', '\\bmi\\gd']
    subprocess.run(comm)
    # time.sleep(2)
    # os.system(f"TASKKILL /F /PID {pid_id}")
    time.sleep(2)
    comm = ['SCHTASKS', '/Run', '/TN', '\\bmi\\gd']
    subprocess.run(comm)
    os.system("TASKKILL /F /IM chromedriver.exe /T")
    os.system("TASKKILL /F /IM chrome.exe /T")
    if message.chat.id != 368246133:
        bot.send_message(message.chat.id, 'Bot restarted')
    bot.send_message(368246133, 'Bot restarted')


@bot.message_handler(commands=['restart_roboforex'])
def restart(message):
    comm = ['SCHTASKS', '/End', '/TN', '\\bmi\\roboforex_checker']
    subprocess.run(comm)
    comm = ['SCHTASKS', '/End', '/TN', '\\bmi\\roboforex_checker_bot']
    subprocess.run(comm)
    os.system("TASKKILL /F /IM chromedriver.exe /T")
    os.system("TASKKILL /F /IM chrome.exe /T")
    time.sleep(2)
    comm = ['SCHTASKS', '/Run', '/TN', '\\bmi\\roboforex_checker']
    subprocess.run(comm)
    comm = ['SCHTASKS', '/Run', '/TN', '\\bmi\\roboforex_checker_bot']
    subprocess.run(comm)
    if message.chat.id != 368246133:
        bot.send_message(message.chat.id, 'Bot restarted')
    bot.send_message(368246133, 'Bot restarted')


'''@bot.message_handler(commands=['start_ban'])
def start(message):
    comm = ['SCHTASKS', '/Run', '/TN', '\\bmi\\test_bmi\\ban_bot']
    subprocess.run(comm)
    os.system("TASKKILL /F /IM chromedriver.exe /T")
    os.system("TASKKILL /F /IM chrome.exe /T")
    if message.chat.id != 368246133:
        bot.send_message(message.chat.id, 'Bot started')
    bot.send_message(368246133, 'Bot started')


@bot.message_handler(commands=['start_uz'])
def start(message):
    comm = ['SCHTASKS', '/Run', '/TN', '\\bmi\\test_bmi\\uz']
    subprocess.run(comm)
    os.system("TASKKILL /F /IM chromedriver.exe /T")
    os.system("TASKKILL /F /IM chrome.exe /T")
    if message.chat.id != 368246133:
        bot.send_message(message.chat.id, 'Bot started')
    bot.send_message(368246133, 'Bot started')'''

bot.polling(none_stop=True)
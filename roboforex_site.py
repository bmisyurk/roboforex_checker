import re
import json
import time
import logging
from selenium import webdriver
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from telebot import TeleBot

with open('credentials_for_bot.json', 'r', encoding='utf-8') as bot_file, \
        open('config.json', 'r', encoding='utf-8') as config_file:
    credentials_bot = json.load(bot_file)
    config_file = json.load(config_file)

bot = TeleBot(credentials_bot["telegram"]["roboforex_bot"], skip_pending=True)
accounts = [37034942, 32033471, 47031446, 47030980]
login = credentials_bot["rb"]["login"]
password = credentials_bot["rb"]["password"]

options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_argument('headless')


def check_file_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config


def login_auth(driver):
    login_input = driver.find_element_by_css_selector('#login-email')
    login_input.click()
    time.sleep(1)
    login_input.send_keys(login)
    pass_input = driver.find_element_by_css_selector('#login-password')
    pass_input.click()
    time.sleep(1)
    pass_input.send_keys(password)
    time.sleep(1)
    driver.find_element_by_css_selector('#login-submit').click()
    time.sleep(5)


def main():
    attemp = 0
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get('https://my.roboforex.com/en/operations/withdraw-funds/form/ccard-out-bz/')
    time.sleep(15)
    try:
        login_auth(driver)
    except Exception as e:
        bot.send_message(credentials_bot["telegram"]["user_bmi"], text=f'Problem with logging: {e}')
    driver.get('https://my.roboforex.com/en/operations/withdraw-funds/form/ccard-out-bz/')
    time.sleep(3)
    while True:
        for account in accounts:
            try:
                driver.find_element_by_css_selector('div.count-select').click()
                time.sleep(1)
                driver.find_element_by_css_selector(
                    f'''div.uk-dropdown-autoflip a[onclick*="CurrentAccount.change('{account}');"]''').click()
                time.sleep(3)
                balance = driver.find_element_by_css_selector('div[data-auto-balance]').text
                currency = re.search('USD|EUR', balance).group(0)
                balance = int(float(re.match('\d+\,*\d*', balance).group(0).replace(',', '.')) * 10)

                withdraw = driver.find_element_by_css_selector(
                    'input#max_withdrawal_amount').get_attribute('value')
                withdraw = int(float(withdraw))
                print(f'Account: {account}')
                print(f'Balance: {balance}')
                print(f'Withdraw {withdraw}')
                drawdown = calc_drawdown(balance, withdraw)
                logging.info(f'Request successufully. Account: {account}, drawdown: {drawdown}%.')
                if drawdown > check_file_config()[f'{account}']['percent'] and check_file_config()[
                    "active"]:
                    bot.send_message(credentials_bot["telegram"]["user_bmi"],
                                     text=f"❗️❗️❗️\nAccount {account}."
                                          f"\n<b>Drawdown is {drawdown}% now.</b>"
                                          f"\nBalance: {balance}{currency}."
                                          f"\nAvaliable withdraw: {withdraw}{currency}."
                                          f"\nCheck please.", parse_mode='html')
            except Exception as e:
                attemp += 1
                if attemp < 2:
                    bot.send_message(credentials_bot["telegram"]["user_bmi"], text=e)
                    time.sleep(30)
                else:
                    driver.close()
                    raise IndexError('Something was wrong')
        time.sleep(check_file_config()["interval"])


def calc_drawdown(balance, withdraw):
    drawdown = int((1 - (withdraw / balance)) * 100)
    return drawdown


if __name__ == "__main__":
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)  # or whatever
    handler = logging.FileHandler('logs/' + datetime.now().strftime('%Y-%m-%d') + '.txt', 'a', 'utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))  # or whatever
    root_logger.addHandler(handler)
    try:
        main()
    except Exception as e:
        bot.send_message(credentials_bot["telegram"]["user_bmi"], text=f'Main error: {e}')
import telebot
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

api_token = config['Telegram']['token']
bot = telebot.TeleBot(api_token)

db_dir = config['Telegram']['db_dir']
link = config['Telegram']['link']
group_id = int(config['Telegram']['group_id'])
admin_id = int(config['Telegram']['admin_id'])

berserker = False
num_reports = 5
ban_time = 300

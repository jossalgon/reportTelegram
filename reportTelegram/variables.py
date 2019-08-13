import configparser

config = configparser.ConfigParser()
config.read('config.ini')

link = config['Telegram']['link']
group_id = int(config['Telegram']['group_id'])
admin_id = int(config['Telegram']['admin_id'])
sticker = config['Telegram']['sticker']


DB_HOST = config['Database']['DB_HOST']
DB_USER = config['Database']['DB_USER']
DB_PASS = config['Database']['DB_PASS']
DB_NAME = config['Database']['DB_NAME']
DB_PORT = config['Database']['DB_PORT']

user_data_dict = dict()

num_reports = 5
ban_time = 300

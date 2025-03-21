import os
from dotenv import load_dotenv

load_dotenv()

# Telegram configuration
link = os.getenv('TELEGRAM_LINK')
group_id = int(os.getenv('TELEGRAM_GROUP_ID'))
admin_id = int(os.getenv('TELEGRAM_ADMIN_ID'))
sticker = os.getenv('TELEGRAM_STICKER')

# Database configuration
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = int(os.getenv('DB_PORT', '3306'))

user_data_dict = dict()

num_reports = 5
ban_time = 300

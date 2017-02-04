# -*- encoding: utf-8 -*-

import configparser
import logging

from telegram.ext import Updater, CommandHandler

from reportTelegram import admin
from reportTelegram import reports
from reportTelegram import variables
from reportTelegram import utils

config = configparser.ConfigParser()
config.read('config.ini')

TG_TOKEN = config['Telegram']['token']

admin_id = variables.admin_id
group_id = variables.group_id

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    message = update.message
    bot.sendMessage(chat_id=message.chat_id, text='Welcome!', reply_to_message_id=message.message_id)


def report(bot, update):
    message = update.message
    if not utils.filter_report(message):
        return False
    user_id = message.from_user.id
    command = message.text.split('@')[0]
    name = command.replace('/', '').capitalize()
    reported = utils.get_user_id(name)
    reports.send_report(bot, user_id, reported)


def stats(bot, update):
    message = update.message
    res = reports.get_stats()
    bot.send_message(message.chat.id, res, parse_mode='Markdown')


def top_kicks(bot, update):
    message = update.message
    res = reports.get_top_kicks()
    bot.send_message(message.chat_id, res, parse_mode='Markdown')


def who(bot, update):
    message = update.message
    res = reports.who(message.from_user.id)
    bot.send_message(message.chat_id, res, parse_mode='Markdown', reply_to_message_id=message.message_id)


def set_reports(bot, update, args):
    message = update.message
    num_reports = args[0]
    if message.from_user.id != admin_id:
        return False
    if num_reports.isdigit():
        res = admin.set_num_reports_by_bot(int(num_reports))
        chat_id = group_id
    else:
        res = 'Send me a number like "/reports 5"'
        chat_id = message.chat_id
    bot.send_message(chat_id, res)


def set_ban_time(bot, update, args):
    message = update.message
    seconds = args[0]
    if message.from_user.id != admin_id:
        return False
    if seconds.isdigit():
        res = admin.set_ban_time(int(seconds))
        chat_id = group_id
    else:
        res = 'Send me a number like "/bantime 5"'
        chat_id = message.chat_id
    bot.send_message(chat_id, res)


def log_error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    utils.create_database()
    updater = Updater(token=TG_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('stats', stats))
    dp.add_handler(CommandHandler('expulsados', top_kicks))
    dp.add_handler(CommandHandler('who', who))
    dp.add_handler(CommandHandler('reports', set_reports, pass_args=True))
    dp.add_handler(CommandHandler('bantime', set_ban_time, pass_args=True))

    for name in utils.get_names():
        dp.add_handler(CommandHandler(name.lower(), report))

    dp.add_error_handler(log_error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

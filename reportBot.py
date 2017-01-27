# -*- encoding: utf-8 -*-

import time

import variables
from src.admin import Admin
from src.reports import Reports
from src.utils import Utils

admin = Admin()
reports = Reports()
utils = Utils()

bot = variables.bot
admin_id = variables.admin_id
group_id = variables.group_id


while True:
    try:
        @bot.message_handler(commands=['help', 'start'])
        def send_welcome(message):
            bot.reply_to(message, 'Welcome!')
            print(group_id)
            print(message.chat.id)

        # REPORTS

        @bot.message_handler(
            commands=['user1', 'user2', 'user3'],
            func=lambda msg: utils.is_from_group(msg.from_user.id) and msg.chat.id == group_id)
        def send_report(message):
            user_id = message.from_user.id
            command = message.text.split('@')[0]
            name = command.replace('/', '').capitalize()
            reported = utils.get_user_id(name)
            reports.send_report(user_id, reported)

        @bot.message_handler(commands=['stats'], func=lambda msg: utils.is_from_group(msg.from_user.id))
        def get_stats(message):
            reports.get_stats(message)

        @bot.message_handler(commands=['expulsados'], func=lambda msg: utils.is_from_group(msg.from_user.id))
        def expulsados_handler(message):
            reports.expulsados_handler(message)

        @bot.message_handler(commands=['who'], func=lambda msg: utils.is_from_group(msg.from_user.id))
        def who(message):
            reports.who(message)

        @bot.message_handler(commands=['reportes'], func=lambda msg: msg.from_user.id == admin_id)
        def set_reportes(message):
            admin.set_num_reports_by_bot(message)


        @bot.message_handler(commands=['time'], func=lambda msg: msg.from_user.id == admin_id)
        def set_ban_time_by_bot(message):
            admin.set_ban_time_by_bot(message)

        def main():
            try:
                utils.create_database()
                for u in utils.get_userIds():
                    bot.unban_chat_member(group_id, u)
            except Exception as exception:
                print(str(exception))


        if __name__ == '__main__':
            main()

        bot.polling(none_stop=True)

    except Exception as e:
        print('Error: %s\nReiniciando en 10seg' % str(e))
        time.sleep(10)

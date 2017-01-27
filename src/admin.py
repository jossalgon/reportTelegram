import time

import variables
from src.utils import Utils

utils = Utils()

bot = variables.bot
admin_id = variables.admin_id
group_id = variables.group_id


class Admin:
    def set_ban_time_by_bot(self, message):
        new_time = message.text[6::]
        if new_time.isdigit() and int(new_time) > 0:
            variables.ban_time = int(new_time)
            m, s = divmod(variables.ban_time, 60)
            ban_time_text = '%01d:%02d' % (m, s)
            bot.send_message(group_id, 'BAN TIME A {0} MINUTOS'.format(ban_time_text))

    def set_num_reports_by_bot(self, message):
        new_reports = message.text[10::]
        if new_reports.isdigit() and int(new_reports) > 0:
            variables.num_reports = int(new_reports)
            bot.send_message(group_id, 'REPORTES A {0}'.format(variables.num_reports))

    def berserker_on(self, message):
        bot.reply_to(message, 'ACTIVANDO MODO BERSERKER...')
        time.sleep(3)
        variables.berserker = True
        bot.send_message(group_id, 'MODO BERSERKER ACTIVADO 10 SEGUNDOS')
        time.sleep(10)
        variables.berserker = False
        bot.send_message(group_id, 'MODO BERSERKER DESACTIVADO')

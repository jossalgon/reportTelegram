import time

from reportTelegram import variables

admin_id = variables.admin_id
group_id = variables.group_id


def set_ban_time(new_time):
    variables.ban_time = int(new_time)
    m, s = divmod(variables.ban_time, 60)
    ban_time_text = '%01d:%02d' % (m, s)
    return 'BAN TIME A {0} MINUTOS'.format(ban_time_text)


def set_num_reports_by_bot(new_reports):
    variables.num_reports = new_reports
    return 'REPORTES A {0}'.format(variables.num_reports)


def berserker_on(bot, message):
    bot.reply_to(message, 'ACTIVANDO MODO BERSERKER...')
    time.sleep(3)
    variables.berserker = True
    bot.send_message(group_id, 'MODO BERSERKER ACTIVADO 10 SEGUNDOS')
    time.sleep(10)
    variables.berserker = False
    bot.send_message(group_id, 'MODO BERSERKER DESACTIVADO')

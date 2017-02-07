# -*- encoding: utf-8 -*-
import io
import logging
import pkgutil
import threading
import time

import pymysql
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from reportTelegram import utils
from reportTelegram import variables

admin_id = variables.admin_id
group_id = variables.group_id
STICKER = variables.sticker

DB_HOST = variables.DB_HOST
DB_USER = variables.DB_USER
DB_PASS = variables.DB_PASS
DB_NAME = variables.DB_NAME

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def get_stats():
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    stats = ''
    try:
        with con.cursor() as cur:
            cur.execute(
                'SELECT COUNT(reported), Name FROM Users u LEFT OUTER JOIN Reports r ON u.UserId = r.reported GROUP BY Name ORDER BY Name')
            rows = cur.fetchall()
            for row in rows:
                num_reportes = row[0]
                name = row[1]
                if num_reportes == variables.num_reports - 1:
                    stats += '\n*%d --> %s*' % (num_reportes, name)
                else:
                    stats += '\n%d --> %s' % (num_reportes, name)
            m, s = divmod(variables.ban_time, 60)
            ban_time_text = '%01d:%02d' % (m, s)
            stats += '\n\n❗️Reportes a %d con ban time de %s minutos.' % (variables.num_reports, ban_time_text)
            return stats
    except Exception:
        logger.error('Fatal error in get_stats', exc_info=True)
    finally:
        if con:
            con.close()


def get_top_kicks():
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    try:
        with con.cursor() as cur:
            cur.execute(
                'SELECT Name, Kicks FROM Users u INNER JOIN Flamers f ON u.UserId = f.UserId GROUP BY Name, Kicks ORDER BY Kicks DESC')
            rows = cur.fetchall()
            top = '😈 Top Seres Oscuros:\n*1º - %s (%d kicks)*\n' % (rows[0][0], rows[0][1])
            for row, pos in zip(rows[1:], range(2, 13)):
                top += '%dº - %s (%d kicks)\n' % (pos, row[0], row[1])
            return top
    except Exception:
        logger.error('Fatal error in get_top_kicks', exc_info=True)
    finally:
        if con:
            con.close()


def who(user_id):
    reportados = 'En total has reportado a:'
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    try:
        with con.cursor() as cur:
            cur.execute('SELECT Reported FROM Reports WHERE UserId = %s', (str(user_id),))
            rows = cur.fetchall()
            for row_l in rows:
                row = row_l[0]
                if row == rows[0][0]:
                    reportados += ' %s' % utils.get_name(row)
                else:
                    reportados += ', %s' % utils.get_name(row)
            if len(rows) > 0:
                return reportados
            else:
                return 'No has reportado a nadie, eres un ser de luz'
    except Exception:
        logger.error('Fatal error in who', exc_info=True)
    finally:
        if con:
            con.close()


def counter(bot, name, reported):
    ban_time = variables.ban_time
    m, s = divmod(ban_time, 60)
    text = 'Expulsado durante: %02d:%02d' % (m, s)
    bot.send_message(group_id, 'A tomar por culo %s' % name)
    bot.kick_chat_member(group_id, reported)
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    try:
        with con.cursor() as cur:
            cur.execute('UPDATE Flamers SET Kicks = Kicks + 1 WHERE UserId = %s', (str(reported),))
            con.commit()
            sti = io.BufferedReader(io.BytesIO(pkgutil.get_data('reportTelegram', 'data/stickers/%s.webp' % STICKER)))
            sti2 = io.BufferedReader(io.BytesIO(pkgutil.get_data('reportTelegram', 'data/stickers/%s.webp' % STICKER)))
            bot.send_sticker(variables.group_id, sti)
            bot.send_sticker(reported, sti2)
            sti.close()
            sti2.close()
            msg = bot.send_message(reported, text)

            while ban_time > 0:
                time.sleep(1)
                ban_time -= 1
                m, s = divmod(ban_time, 60)
                text = 'Expulsado durante: %02d:%02d' % (m, s)
                bot.edit_message_text(text, chat_id=reported, message_id=msg.message_id)
            bot.unban_chat_member(group_id, reported)
            cur.execute('DELETE FROM Reports WHERE Reported = %s', (str(reported),))
            button = InlineKeyboardButton('Invitación', url=variables.link)
            markup = InlineKeyboardMarkup([[button]])
            bot.send_message(reported, 'Ya puedes entrar %s, usa esta invitación:' % name, reply_markup=markup)
    except Exception:
        logger.error('Fatal error in counter', exc_info=True)
    finally:
        if con:
            con.commit()
            con.close()


def send_report(bot, user_id, reported):
    name = utils.get_name(reported)
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    try:
        with con.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM Reports WHERE Reported = %s', (str(reported),))
            num_reportes = int(cur.fetchone()[0])
            cur.execute('SELECT COUNT(*) FROM Reports WHERE Reported = %s AND UserId = %s',
                        (str(reported), str(user_id)))
            already_reported = bool(cur.fetchone()[0])
            if num_reportes == variables.num_reports:  # Si ya tiene 5 reportes
                bot.send_message(group_id, 'Ensañamiento!!!')
            elif not already_reported and user_id != reported:
                if num_reportes == (variables.num_reports - 1):  # si le queda un reporte para ser expulsado
                    cur.execute('INSERT INTO Reports VALUES(%s,%s)', (str(reported), str(user_id)))
                    thr1 = threading.Thread(target=counter, args=(bot, name, reported))
                    thr1.start()
                elif num_reportes < (variables.num_reports - 1):  # si le quedan mas de un reporte para ser expulsado
                    cur.execute('INSERT INTO Reports VALUES(%s,%s)', (str(reported), str(user_id)))
                    bot.send_message(group_id, '⚠️ %s fue reportado (%d)' % (name, num_reportes + 1))
            elif user_id != reported:  # si es miembro del grupo y no es autoreporte y viene del grupo
                bot.send_message(group_id, 'Ya has reportado a %s' % name)
    except Exception:
        logger.error('Fatal error in send_report', exc_info=True)
    finally:
        if con:
            con.commit()
            con.close()


def send_love(bot, user_id, loved):
    name = utils.get_name(loved)
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    try:
        with con.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM Reports WHERE Reported = %s', (str(loved),))
            num_reportes = int(cur.fetchone()[0])
            cur.execute('SELECT COUNT(*) FROM Reports WHERE Reported = %s AND UserId = %s',
                        (str(loved), str(user_id)))
            already_reported = bool(cur.fetchone()[0])
            if num_reportes == variables.num_reports:  # Si ya tiene 5 reportes
                bot.send_message(group_id, 'Abrazos!!!')
            elif already_reported and user_id != loved:
                cur.execute('DELETE FROM Reports WHERE Reported = %s AND UserId = %s', (str(loved), str(user_id)))
                bot.send_message(group_id, '❤️️ %s recibió mucho amor (Reportes: %d)' % (name, num_reportes - 1))
            elif user_id == loved:  # si es miembro del grupo y no es autoreporte y viene del grupo
                bot.send_message(group_id, '✊ Te diste mucho amoooor, dios si mucho amor mmmmm')
            elif user_id != loved:  # si es miembro del grupo y no es autoreporte y viene del grupo
                bot.send_message(group_id, '💋 Le diste un buen beso en la picota a %s' % name)
    except Exception:
        logger.error('Fatal error in send_love', exc_info=True)
    finally:
        if con:
            con.commit()

# -*- encoding: utf-8 -*-

import pymysql
import threading
import time

from telebot import types

import variables
from src.utils import Utils

utils = Utils()

bot = variables.bot
admin_id = variables.admin_id
group_id = variables.group_id
n_reportes = variables.num_reports

DB_HOST = variables.DB_HOST
DB_USER = variables.DB_USER
DB_PASS = variables.DB_PASS
DB_NAME = variables.DB_NAME


class Reports:
    def get_stats(self, message):
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
                    if num_reportes == n_reportes - 1:
                        stats += '\n*%d --> %s*' % (num_reportes, name)
                    else:
                        stats += '\n%d --> %s' % (num_reportes, name)
                m, s = divmod(variables.ban_time, 60)
                ban_time_text = '%01d:%02d' % (m, s)
                stats += '\n\n❗️Reportes a %d con ban time de %s minutos.' % (n_reportes, ban_time_text)
                bot.send_message(message.chat.id, stats, parse_mode='Markdown')
        except Exception as exception:
            bot.send_message(admin_id, exception)
        finally:
            if con:
                con.close()

    def expulsados_handler(self, message):
        chat_id = message.chat.id
        con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        try:
            with con.cursor() as cur:
                cur.execute(
                    'SELECT Name, Kicks FROM Users u INNER JOIN Flamers f ON u.UserId = f.UserId GROUP BY Name, Kicks ORDER BY Kicks DESC')
                rows = cur.fetchall()
                top = '😈 Top Seres Oscuros:\n*1º - %s (%d kicks)*\n' % (rows[0][0], rows[0][1])
                for row, pos in zip(rows[1:], range(2, 13)):
                    top += '%dº - %s (%d kicks)\n' % (pos, row[0], row[1])
                bot.send_message(chat_id, top, parse_mode='Markdown')
        except Exception as exception:
            bot.send_message(admin_id, exception)
        finally:
            if con:
                con.close()

    def who(self, message):
        user_id = message.from_user.id
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
                    bot.reply_to(message, reportados)
                else:
                    bot.reply_to(message, 'No has reportado a nadie, eres un ser de luz')
        except Exception as exception:
            bot.send_message(admin_id, exception)
        finally:
            if con:
                con.close()

    def cuenta(self, name, reported):
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
                sti = open('data/stickers/nancy.webp', 'rb')
                sti2 = open('data/stickers/nancy.webp', 'rb')
                bot.send_sticker(group_id, sti)
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
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Invitación', url=variables.link))
                bot.send_message(reported, 'Ya puedes entrar %s, usa esta invitación:' % name, reply_markup=markup)
        except Exception as e:
            bot.send_message(admin_id, 'Hubo un fallo con %s dentro de 5min se desbaneará\nError: %s' % (name, str(e)))
            time.sleep(300)
            bot.unban_chat_member(group_id, reported)
        finally:
            if con:
                con.commit()
                con.close()

    def send_report(self, user_id, reported):
        name = utils.get_name(reported)
        con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        try:
            with con.cursor() as cur:
                cur.execute('SELECT COUNT(*) FROM Reports WHERE Reported = %s', (str(reported),))
                num_reportes = int(cur.fetchone()[0])
                cur.execute('SELECT COUNT(*) FROM Reports WHERE Reported = %s AND UserId = %s',
                            (str(reported), str(user_id)))
                already_reported = bool(cur.fetchone()[0])
                if num_reportes == n_reportes:  # Si ya tiene 5 reportes
                    bot.send_message(group_id, 'Ensañamiento!!!')
                elif (not already_reported or variables.berserker) and user_id != reported:
                    if num_reportes == (n_reportes - 1):  # si le queda un reporte para ser expulsado
                        cur.execute('INSERT INTO Reports VALUES(%s,%s)', (str(reported), str(user_id)))
                        thr1 = threading.Thread(target=self.cuenta, args=(name, reported))
                        thr1.start()
                    elif num_reportes < (n_reportes - 1):  # si le quedan mas de un reporte para ser expulsado
                        cur.execute('INSERT INTO Reports VALUES(%s,%s)', (str(reported), str(user_id)))
                        bot.send_message(group_id, '⚠️ %s fue reportado (%d)' % (name, num_reportes + 1))
                elif user_id != reported:  # si es miembro del grupo y no es autoreporte y viene del grupo
                    bot.send_message(group_id, 'Ya has reportado a %s' % name)
        except Exception as exception:
            bot.send_message(admin_id, exception)
        finally:
            if con:
                con.commit()
                con.close()

    def send_love(self, user_id, loved):
        name = utils.get_name(loved)
        con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        try:
            with con.cursor() as cur:
                cur.execute('SELECT COUNT(*) FROM Reports WHERE Reported = %s', (str(loved),))
                num_reportes = int(cur.fetchone()[0])
                cur.execute('SELECT COUNT(*) FROM Reports WHERE Reported = %s AND UserId = %s',
                            (str(loved), str(user_id)))
                already_reported = bool(cur.fetchone()[0])
                if num_reportes == n_reportes:  # Si ya tiene 5 reportes
                    bot.send_message(group_id, 'Abrazos!!!')
                elif already_reported and user_id != loved:
                    cur.execute('DELETE FROM Reports WHERE Reported = %s AND UserId = %s', (str(loved), str(user_id)))
                    bot.send_message(group_id, '❤️️ %s recibió mucho amor (Reportes: %d)' % (name, num_reportes - 1))
                elif user_id == loved:  # si es miembro del grupo y no es autoreporte y viene del grupo
                    bot.send_message(group_id, '✊ Te diste mucho amoooor, dios si mucho amor mmmmm')
                elif user_id != loved:  # si es miembro del grupo y no es autoreporte y viene del grupo
                    bot.send_message(group_id, '💋 Le diste un buen beso en la picota a %s' % name)
        except Exception as exception:
            bot.send_message(admin_id, exception)
        finally:
            if con:
                con.commit()

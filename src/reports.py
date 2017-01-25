# -*- encoding: utf-8 -*-

import sqlite3 as lite
import threading
import time

from telebot import types

import variables
from src.utils import Utils

utils = Utils()

bot = variables.bot
admin_id = variables.admin_id
group_id = variables.group_id
db_dir = variables.db_dir
n_reportes = variables.num_reports


class Reports:
    def get_stats(self, message):
        con = lite.connect(db_dir)
        stats = ''
        try:
            cur = con.cursor()
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
            print(exception)
        finally:
            if con:
                con.close()

    def expulsados_handler(self, message):
        chat_id = message.chat.id
        con = lite.connect(db_dir)
        try:
            cur = con.cursor()
            cur.execute(
                'SELECT Name, Kicks FROM Users u INNER JOIN Flamers f ON u.UserId = f.UserId GROUP BY Name ORDER BY Kicks DESC')
            rows = cur.fetchall()
            top = '😈 Top Seres Oscuros:\n*1º - %s (%d kicks)*\n' % (rows[0][0], rows[0][1])
            for row, pos in zip(rows[1:], range(2, 13)):
                top += '%dº - %s (%d kicks)\n' % (pos, row[0], row[1])
            bot.send_message(chat_id, top, parse_mode='Markdown')
        except Exception as exception:
            print(exception)
        finally:
            if con:
                con.close()

    def who(self, message):
        user_id = message.from_user.id
        reportados = 'En total has reportado a:'
        con = lite.connect(db_dir)
        try:
            cur = con.cursor()
            cur.execute('SELECT Reported FROM Reports WHERE UserId = ?', (user_id,))
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
            print(exception)
        finally:
            if con:
                con.close()

    def cuenta(self, name, reported):
        ban_time = variables.ban_time
        m, s = divmod(ban_time, 60)
        text = 'Expulsado durante: %02d:%02d' % (m, s)
        bot.send_message(group_id, 'A tomar por culo %s' % name)
        bot.kick_chat_member(group_id, reported)
        con = lite.connect(db_dir)
        cur = con.cursor()
        try:
            cur.execute('UPDATE Flamers SET Kicks = Kicks + 1 WHERE UserId = ?', (reported,))
            con.commit()
            msg = bot.send_message(reported, text)
        except:
            msg = bot.send_message(admin_id, 'Hubo un fallo con %s dentro de 5min se desbaneará' % name)
            time.sleep(300)
            bot.unban_chat_member(group_id, reported)
            cur.execute('DELETE FROM Reports WHERE Reported = ?;', (reported,))
            con.commit()
            if con:
                con.close()
        try:
            while ban_time > 0:
                time.sleep(1)
                ban_time -= 1
                m, s = divmod(ban_time, 60)
                text = 'Expulsado durante: %02d:%02d' % (m, s)
                bot.edit_message_text(text, chat_id=reported, message_id=msg.message_id)
            bot.unban_chat_member(group_id, reported)
            cur.execute('DELETE FROM Reports WHERE Reported = ?;', (reported,))
            con.commit()
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Invitación', url=variables.link))
            bot.send_message(reported, 'Ya puedes entrar %s, usa esta invitación:' % name, reply_markup=markup)
        except Exception as exception:
            print('Fallo en contador de %s\n%s' % (name, exception))
        finally:
            if con:
                con.close()

    def send_report(self, user_id, reported):
        name = utils.get_name(reported)
        con = lite.connect(db_dir)
        try:
            cur = con.cursor()
            cur.execute('SELECT COUNT(*) FROM Reports WHERE Reported = ?', (reported,))
            num_reportes = int(cur.fetchone()[0])
            cur.execute('SELECT COUNT(*) FROM Reports WHERE Reported = ? AND UserId = ?', (reported, user_id))
            already_reported = bool(cur.fetchone()[0])
            if num_reportes == n_reportes:  # Si ya tiene 5 reportes
                bot.send_message(group_id, 'Ensañamiento!!!')
            elif (not already_reported or variables.berserker) and user_id != reported:
                if num_reportes == (n_reportes - 1):  # si le queda un reporte para ser expulsado
                    cur.execute('INSERT INTO Reports VALUES(?,?)', (reported, user_id))
                    thr1 = threading.Thread(target=self.cuenta, args=(name, reported))
                    thr1.start()
                elif num_reportes < (n_reportes - 1):  # si le quedan mas de un reporte para ser expulsado
                    cur.execute('INSERT INTO Reports VALUES(?,?)', (reported, user_id))
                    bot.send_message(group_id, '⚠️ %s fue reportado (%d)' % (name, num_reportes + 1))
            elif user_id != reported:  # si es miembro del grupo y no es autoreporte y viene del grupo
                bot.send_message(group_id, 'Ya has reportado a %s' % name)
        except Exception as exception:
            print(exception)
        finally:
            if con:
                con.commit()
                con.close()

    def send_love(self, user_id, loved):
        name = utils.get_name(loved)
        con = lite.connect(db_dir)
        try:
            cur = con.cursor()
            cur.execute('SELECT COUNT(*) FROM Reports WHERE Reported = ?', (loved,))
            num_reportes = int(cur.fetchone()[0])
            cur.execute('SELECT COUNT(*) FROM Reports WHERE Reported = ? AND UserId = ?', (loved, user_id))
            already_reported = bool(cur.fetchone()[0])
            if num_reportes == n_reportes:  # Si ya tiene 5 reportes
                bot.send_message(group_id, 'Abrazos!!!')
            elif already_reported and user_id != loved:
                cur.execute('DELETE FROM Reports WHERE Reported = ? AND UserId = ?', (loved, user_id))
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
                con.close()

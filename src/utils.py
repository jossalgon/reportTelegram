import sqlite3 as lite

import variables

bot = variables.bot
ADMIN_ID = variables.admin_id
GROUP_ID = variables.group_id
DB_DIR = variables.db_dir


class Utils:
    def get_name(self, user_id):
        username = 'Anon'
        con = lite.connect(DB_DIR)
        try:
            with con:
                cur = con.cursor()
                cur.execute('SELECT Name FROM Users WHERE UserId = ?', (user_id,))
                username = cur.fetchone()[0]
        except Exception as exception:
            bot.send_message(ADMIN_ID, exception)
        return username

    def get_user_id(self, name):
        user_id = 0
        con = lite.connect(DB_DIR)
        try:
            with con:
                cur = con.cursor()
                cur.execute('SELECT UserId FROM Users WHERE Name = ?', (name,))
                user_id = int(cur.fetchone()[0])
        except Exception as exception:
            bot.send_message(ADMIN_ID, exception)
        return user_id

    def is_from_group(self, user_id):
        result = False
        con = lite.connect(DB_DIR)
        try:
            with con:
                cur = con.cursor()
                cur.execute('SELECT EXISTS(SELECT 1 FROM Users WHERE UserId = ?)', (user_id,))
                result = bool(cur.fetchone()[0])
        except Exception as exception:
            bot.send_message(ADMIN_ID, exception)
        return result

    def get_userIds(self):
        userIds = []
        con = lite.connect(DB_DIR)
        try:
            with con:
                cur = con.cursor()
                cur.execute('SELECT UserId FROM Users')
                rows = cur.fetchall()
                for row in rows:
                    userIds.append(row[0])
        except Exception as exception:
            bot.send_message(ADMIN_ID, exception)
        return userIds

    def get_usernames(self):
        usernames = {}
        for user_id in self.get_userIds():
            if user_id not in self.get_not_mention():
                username = bot.get_chat_member(GROUP_ID, user_id).user.username
                usernames['@%s' % username] = user_id
        return usernames

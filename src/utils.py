import pymysql

import variables

bot = variables.bot
ADMIN_ID = variables.admin_id
GROUP_ID = variables.group_id

DB_HOST = variables.DB_HOST
DB_USER = variables.DB_USER
DB_PASS = variables.DB_PASS
DB_NAME = variables.DB_NAME

class Utils:
    def get_name(self, user_id):
        username = 'Anon'
        con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        try:
            with con.cursor() as cur:
                cur.execute('SELECT Name FROM Users WHERE UserId = %s', (str(user_id),))
                username = cur.fetchone()[0]
        except Exception as exception:
            bot.send_message(ADMIN_ID, exception)
        finally:
            if con:
                con.close()
            return username

    def get_user_id(self, name):
        user_id = 0
        con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        try:
            with con.cursor() as cur:
                cur.execute('SELECT UserId FROM Users WHERE Name = %s', (str(name),))
                user_id = int(cur.fetchone()[0])
        except Exception as exception:
            bot.send_message(ADMIN_ID, exception)
        finally:
            if con:
                con.close()
            return user_id

    def is_from_group(self, user_id):
        result = False
        con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        try:
            with con.cursor() as cur:
                cur.execute('SELECT EXISTS(SELECT 1 FROM Users WHERE UserId = %s)', (str(user_id),))
                result = bool(cur.fetchone()[0])
        except Exception as exception:
            bot.send_message(ADMIN_ID, exception)
        finally:
            if con:
                con.close()
            return result

    def get_userIds(self):
        user_ids = []
        con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        try:
            with con.cursor() as cur:
                cur.execute('SELECT UserId FROM Users')
                rows = cur.fetchall()
                for row in rows:
                    user_ids.append(row[0])
        except Exception as exception:
            bot.send_message(ADMIN_ID, exception)
        finally:
            if con:
                con.close()
            return user_ids

    def get_usernames(self):
        usernames = {}
        for user_id in self.get_userIds():
            if user_id not in self.get_not_mention():
                username = bot.get_chat_member(GROUP_ID, user_id).user.username
                usernames['@%s' % username] = user_id
        return usernames

    def create_database(self):
        con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
        try:
            with con.cursor() as cur:
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS `Reports` ( \
                      `Reported` int(11) NOT NULL, \
                      `UserId` int(11) NOT NULL \
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; \
                    CREATE TABLE IF NOT EXISTS `Users` ( \
                      `UserId` int(11) NOT NULL, \
                      `Name` text NOT NULL \
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; \
                    ")
        except Exception as exception:
            print(exception)
        finally:
            if con:
                con.commit()
                con.close()

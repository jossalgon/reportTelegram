import logging

import pymysql

from reportTelegram import variables

ADMIN_ID = variables.admin_id
GROUP_ID = variables.group_id

DB_HOST = variables.DB_HOST
DB_USER = variables.DB_USER
DB_PASS = variables.DB_PASS
DB_NAME = variables.DB_NAME

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def filter_report(msg):
    return is_from_group(msg.from_user.id) and msg.chat.id == variables.group_id


def get_name(user_id):
    username = 'Anon'
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    try:
        with con.cursor() as cur:
            cur.execute('SELECT Name FROM Users WHERE UserId = %s', (str(user_id),))
            if cur.rowcount:
                username = cur.fetchone()[0]
    except Exception:
        logger.error('Fatal error in get_name', exc_info=True)
    finally:
        if con:
            con.close()
        return username


def get_user_id(name):
    user_id = 0
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    try:
        with con.cursor() as cur:
            cur.execute('SELECT UserId FROM Users WHERE Name = %s', (str(name),))
            if cur.rowcount:
                user_id = int(cur.fetchone()[0])
    except Exception:
        logger.error('Fatal error in get_user_id', exc_info=True)
    finally:
        if con:
            con.close()
        return user_id


def is_from_group(user_id):
    result = False
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    try:
        with con.cursor() as cur:
            cur.execute('SELECT EXISTS(SELECT 1 FROM Users WHERE UserId = %s)', (str(user_id),))
            result = bool(cur.fetchone()[0])
    except Exception:
        logger.error('Fatal error in is_from_group', exc_info=True)
    finally:
        if con:
            con.close()
        return result


def get_userIds():
    user_ids = []
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    try:
        with con.cursor() as cur:
            cur.execute('SELECT UserId FROM Users')
            rows = cur.fetchall()
            for row in rows:
                user_ids.append(row[0])
    except Exception:
        logger.error('Fatal error in is_from_group', exc_info=True)
    finally:
        if con:
            con.close()
        return user_ids


def get_usernames(bot):
    usernames = {}
    for user_id in get_userIds():
        username = bot.get_chat_member(GROUP_ID, user_id).user.username
        usernames['@%s' % username] = user_id
    return usernames


def get_names():
    names = []
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    try:
        with con.cursor() as cur:
            cur.execute('SELECT Name FROM Users')
            rows = cur.fetchall()
            for row in rows:
                names.append(row[0])
    except Exception as exception:
        print(exception)
    finally:
        if con:
            con.close()
        return names


def create_database():
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

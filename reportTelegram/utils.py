import logging

import pymysql

from reportTelegram import variables

ADMIN_ID = variables.admin_id
GROUP_ID = variables.group_id

DB_HOST = variables.DB_HOST
DB_USER = variables.DB_USER
DB_PASS = variables.DB_PASS
DB_NAME = variables.DB_NAME
DB_PORT = variables.DB_PORT

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def create_connection():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME, port=DB_PORT)


def filter_report(msg):
    return is_from_group(msg.from_user.id) and msg.chat.id == variables.group_id


def clear_report_data(reported):
    user_data = variables.user_data_dict[reported]
    con = create_connection()
    try:
        with con.cursor() as cur:
            cur.execute('DELETE FROM Reports WHERE Reported = %s', (str(reported),))
    except Exception:
        logger.error('Fatal error in clear_report_data', exc_info=True)
    try:
        user_data['ban_time'] = 0
        del user_data['unkick_job']
    except Exception:
        logger.error('Fatal error in clear_report_data variable', exc_info=True)
    finally:
        if con:
            con.commit()
            con.close()


def get_name(user_id):
    username = 'Anon'
    con = create_connection()
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
    con = create_connection()
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
    con = create_connection()
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


def get_names():
    names = []
    con = create_connection()
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


def remove_message_from_group(bot, job):
    bot.delete_message(chat_id=variables.group_id, message_id=job.context)


def create_database():
    con = create_connection()
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

# ReportTelegram
ReportTelegram is a telegram bot that helps you to keep the group clean by a report system with kicks and ban times.

## Installing
1. Install or upgrade reportTelegram from pip:
  ```
  $ pip install reportTelegram --upgrade
  ```
Or you can install from source:
  ```
  $ git clone https://github.com/jossalgon/reportTelegram.git
  $ cd reportTelegram
  $ python setup.py install
  ```

2. Create a config.ini file:

  ```
  [Telegram]
  token_id = YOUR_TELEGRAM_BOT_TOKEN
  link = YOUR_GROUP_LINK
  group_id =  YOUR_GROUP_ID
  admin_id = THE_ADMIN_ID
  sticker = banned
  
  [Database]
  DB_HOST = YOUR_DB_HOST
  DB_USER = YOUR_DB_USER
  DB_PASS = YOUR_DB_PASS
  DB_NAME = YOUR_DB_NAME
  DB_PORT = YOUR_DB_PORT
  ```

3. Run the bot
  ```
  python3 -m reportTelegram
  ```

4. Populate database
    
    Populate the Users table with columns UserId and Name you want to use to report.

5. Restart the bot

    Restart the bot to apply the new report commands



## Commands
Command | Uses
------- | -----
/start | Reply with a welcome message
/stats | Reply with report stats
/expulsados | Show a kicked top
/who | Reply with the users that you reported
/reports n | Set max reports to n (where n is a number)
/bantime n | Set kick time to n (where n is the number of seconds)
/user1 | Report user1
/user2 | Report user2
/user3 | Report user3
/...   | Report ...
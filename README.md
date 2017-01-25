# ReportTelegram
ReportTelegram is a telegram bot that helps you to keep the group clean by a report system with kicks and ban times.

## Installation
1. Create a config.ini file with:

  ```
  [Telegram]
  token_id = YOUR_TELEGRAM_BOT_TOKEN
  db_dir = data.db (OR YOUR DATABASE NAME)
  link = YOUR_GROUP_LINK
  group_id =  YOUR_GROUP_ID
  admin_id = THE_ADMIN_ID
  ```

2. Change the "send_report" (reportBot.py) commands handler to usernames of your group.
    ```
    @bot.message_handler(
            commands=['Mark', 'Charlie', 'Alex'],
            func=lambda msg: ...)
        def send_report(message):
           ...
    ```

3. Install requirements
  ```
  sudo pip install -r requirements.txt
  ```

4. Run the bot
  ```
  python3 reportBot.py &
  ```

## Commands
Command | Uses
------- | -----
/start | Reply with a welcome message
/stats | Reply with report stats
/expulsados | Show a kicked top
/who | Reply with the users that you reported
/reportes n | Set max reports to n (where n is a number)
/time n | Set kick time to n (where n is the number of seconds)
/user1 | Report user1
/user2 | Report user2
/user3 | Report user3
/...   | Report ...
import sqlite3

from tg_bot.config import Config


con = sqlite3.connect(Config.DATABASE_NAME) # Create database and open connection
con.row_factory = sqlite3.Row # makes SELECT results behave like dicts (column names as keys) instead of tuples
cur = con.cursor() # Creates cursor object to execute SQL queries

# Creating tables
cur.execute("create table if not exists warnings(" \
            "`chat_id` BIGINT not null," \
            "`user_id` BIGINT not null," \
            "`current_count` tinyint not null default 0," \
            "PRIMARY KEY (chat_id, user_id))")

cur.execute("create table if not exists channel_settings(" \
            "`chat_id` BIGINT not null," \
            f"`language` text default '{Config.DEFAULT_LANGUAGE}'," \
            "`max_warn_count` int default 3," \
            "`soft_warn` bool default false," \
            "`change_settings_creator_only` bool default true," \
            "`welcome_message` text default ''," \
            "primary key(chat_id)" \
            ")")

con.commit()
    
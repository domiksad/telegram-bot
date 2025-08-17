import sqlite3

from tg_bot.modules.sql import con, cur

def create_tables():
    cur.execute("create table warnings(`chat_id` BIGINT not null, `user_id` BIGINT not null, `current_count` tinyint not null default 0, PRIMARY KEY (chat_id, user_id))")
    cur.execute("create table messages(`chat_id` BIGINT not null, `user_id` BIGINT not null, `message_id` BIGINT not null, `sent_at` timestamp , PRIMARY KEY (chat_id, message_id))")

def drop_tables():
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    for table in tables:
        cur.execute(f"DROP TABLE {table[0]};")
    con.commit()

def is_database_empty():
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    if len(tables) == 2: # hardcoded value :(
        return False
    return True


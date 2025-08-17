import sqlite3

from tg_bot.modules.sql import con, cur
from tg_bot.config import Config


def create_tables():
    cur.execute("create table if not exists warnings(`chat_id` BIGINT not null, `user_id` BIGINT not null, `current_count` tinyint not null default 0, PRIMARY KEY (chat_id, user_id))")
    cur.execute("create table if not exists messages(`chat_id` BIGINT not null, `user_id` BIGINT not null, `message_id` BIGINT not null, `sent_at` timestamp , PRIMARY KEY (chat_id, message_id))")
    cur.execute("create table if not exists rules(`chat_id` BIGINT not null, `rule_text` text, PRIMARY KEY (chat_id))")
    con.commit()


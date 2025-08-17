import sqlite3

from tg_bot.config import Config


con = sqlite3.connect(Config.DATABASE_NAME+".db")
cur = con.cursor()

from tg_bot.modules.sql.setup import * # fix circular import
if is_database_empty():
    drop_tables()
    create_tables()
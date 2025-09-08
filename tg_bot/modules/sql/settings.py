from tg_bot.modules.sql import con, cur


def ensure_settings(chat_id: int):
    cur.execute("SELECT * FROM channel_settings WHERE chat_id = ?", [chat_id])
    if cur.fetchone() is None:
        cur.execute("INSERT INTO channel_settings(chat_id) VALUES (?)", [chat_id])
        con.commit()
        return

def get_settings(chat_id: int) -> dict:
    ensure_settings(chat_id=chat_id)
    cur.execute("SELECT * FROM channel_settings WHERE chat_id = ?", [chat_id])
    row = cur.fetchone()
    return dict(row) if row else {}

def get_chat_language(chat_id: int) -> str:
    ensure_settings(chat_id=chat_id)
    cur.execute("SELECT * FROM channel_settings WHERE chat_id = ?", [chat_id])
    row = cur.fetchone()
    return row["language"]

def set_setting(chat_id: int, setting: str, value):
    cur.execute(f"UPDATE channel_settings SET {setting} = ? WHERE chat_id = ?", [value, chat_id])
    con.commit()
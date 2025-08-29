from telegram import Chat, User

from tg_bot.modules.sql import con, cur


def add_warn(chat: Chat, user: User):
    cur.execute("SELECT current_count FROM warnings WHERE chat_id = ? and user_id = ?", [chat.id, user.id])
    row = cur.fetchone()
    if row is None:
        cur.execute("INSERT INTO warnings(chat_id, user_id, current_count) values (?, ?, ?)", [chat.id, user.id, 1])
        con.commit()
        return 1
    
    current_count: int = row[0] + 1
    cur.execute(f"UPDATE warnings SET current_count = {current_count} WHERE chat_id = ? and user_id = ?", [chat.id, user.id])
    con.commit()
    return current_count

def del_warn(chat: Chat, user: User):
    cur.execute("SELECT current_count FROM warnings WHERE chat_id = ? and user_id = ?", [chat.id, user.id])
    row = cur.fetchone()
    if row is None:
        return 0
    
    current_count: int = row[0] - 1
    if current_count <= 0:
        reset_warns(chat=chat, user=user)
        return 0
    cur.execute(f"UPDATE warnings SET current_count = {current_count} WHERE chat_id = ? and user_id = ?", [chat.id, user.id])
    con.commit()
    return current_count

def reset_warns(chat: Chat, user: User):
    cur.execute(f"DELETE FROM warnings WHERE chat_id = ? and user_id = ?", [chat.id, user.id])
    con.commit()
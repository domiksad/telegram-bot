from typing import Tuple

from tg_bot.modules.sql import con, cur


def _record_exists(chat_id: int, user_id: int):
    cur.execute("select * from warnings where chat_id = ? and user_id = ?", [chat_id, user_id])
    if len(cur.fetchall()) >= 1:
        return True
    return False

def check_warn_count(chat_id: int, user_id: int) -> int:
    cur.execute("select current_count from warnings where chat_id = ? and user_id = ?", [chat_id, user_id])
    current_count: int = cur.fetchone()
    return current_count

def increment_warn_count(chat_id: int, user_id: int) -> int:
    if not _record_exists(chat_id=chat_id, user_id=user_id):
        cur.execute("insert into warnings values (?, ?, ?)", [chat_id, user_id, 1])
        con.commit()
        return 1
    
    current_count = check_warn_count(chat_id=chat_id, user_id=user_id)
    cur.execute(f"update warnings set {current_count+1} where chat_id = ? and user_id = ?", [chat_id, user_id])
    con.commit()
    return current_count+1

def decrement_warn_count(chat_id: int, user_id: int) -> int:
    if not _record_exists(chat_id=chat_id, user_id=user_id):
        return 1
    
    current_count = check_warn_count(chat_id=chat_id, user_id=user_id)
    if current_count == 0:
        return -1
    cur.execute(f"update warnings set {current_count-1} where chat_id = ? and user_id = ?", [chat_id, user_id])
    con.commit()
    return current_count-1

def reset_warn_count(chat_id: int, user_id: int):
    cur.execute("delete from warnings where chat_id = ? and user_id = ?", [chat_id, user_id])
    con.commit()

from tg_bot.modules.sql import con, cur


def set_rule(chat_id: int, rule_text: str):
    cur.execute("select rule_text from rules where chat_id = ?", [chat_id])
    row = cur.fetchone()
    if row is None:
        cur.execute("insert into rules values (?, ?)", [chat_id, rule_text])
        con.commit()
        return
    cur.execute("update rules set rule_text = ? where chat_id = ?", [rule_text, chat_id])
    con.commit()
    
def read_rule(chat_id: int) -> str:
    cur.execute("select rule_text from rules where chat_id = ?", [chat_id])
    row = cur.fetchone()
    if row is None:
        return ""
    return row[0]
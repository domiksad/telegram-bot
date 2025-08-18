from tg_bot.modules.sql import con, cur


def set_welcome_message(chat_id: int, welcome_message_text: str):
    if read_welcome_message(chat_id=chat_id) is None:
        cur.execute("insert into welcome_messages values (?, ?)", [chat_id, welcome_message_text])
    else:
        cur.execute("update welcome_messages set welcome_message_text = ? where chat_id = ?", [welcome_message_text, chat_id])
    con.commit()

def read_welcome_message(chat_id: int):
    cur.execute("select welcome_message_text from welcome_messages where chat_id = ?", [chat_id])
    row = cur.fetchone()
    if row is None:
        return None
    return row[0]
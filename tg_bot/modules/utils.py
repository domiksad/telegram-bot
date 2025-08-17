import re

from telegram import User

def escape_markdown(msg: str) -> str:
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', msg)

def mention_user_md(user: User):
    return f"[{escape_markdown(user.full_name)}](tg://user?id={user.id})"
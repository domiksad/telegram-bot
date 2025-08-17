from tg_bot.modules.sql import warns
from tg_bot.modules.sql import rules

def increment_warn_count(chat_id: int, user_id: int) -> int:
    return warns.increment_warn_count(chat_id=chat_id, user_id=user_id)

def decrement_warn_count(chat_id: int, user_id: int) -> int:
    return warns.decrement_warn_count(chat_id=chat_id, user_id=user_id)

def reset_warn_count(chat_id: int, user_id: int):
    return warns.reset_warn_count(chat_id=chat_id, user_id=user_id)

def check_warn_count(chat_id: int, user_id: int) -> int:
    return warns.check_warn_count(chat_id=chat_id, user_id=user_id)

def add_rule_db(chat_id: int, rule: str):
    return rules.set_rule(chat_id=chat_id, rule_text=rule)

def read_rule_db(chat_id: int):
    return rules.read_rule(chat_id=chat_id)
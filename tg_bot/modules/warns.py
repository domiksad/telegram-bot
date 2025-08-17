from typing import Dict, Tuple

from tg_bot.config import Config

if Config.USE_DATABASE:
    from tg_bot.modules import database

# (chat_id, user_id) : warning count
warns_count: Dict[Tuple[int, int], int] = {}

def _increment_warn_count(chat_id: int, user_id: int) -> int:
    key = (chat_id, user_id)
    if key not in warns_count:
        warns_count[key] = 1
    else:
        warns_count[key] += 1
    return warns_count[key] 

def _decrement_warn_count(chat_id: int, user_id: int) -> int:
    key = (chat_id, user_id)
    if key not in warns_count:
        return -1
    elif warns_count[key] > 0:
        warns_count[key] -= 1
        return warns_count[key] 
    return -1

def _reset_warn_count(chat_id: int, user_id: int):
    warns_count[(chat_id, user_id)] = 0

def _check_warn_count(chat_id: int, user_id: int) -> int:
    return warns_count.get((chat_id, user_id), 0)

###

def increment_warn_count(chat_id: int, user_id: int) -> int:
    if Config.USE_DATABASE:
        return database.increment_warn_count(chat_id=chat_id, user_id=user_id)
    else:
        return _increment_warn_count(chat_id=chat_id, user_id=user_id)

def decrement_warn_count(chat_id: int, user_id: int) -> int:
    if Config.USE_DATABASE:
        return database.decrement_warn_count(chat_id=chat_id, user_id=user_id)
    else:
        return _decrement_warn_count(chat_id=chat_id, user_id=user_id)

def reset_warn_count(chat_id: int, user_id: int):
    if Config.USE_DATABASE:
        return database.reset_warn_count(chat_id=chat_id, user_id=user_id)
    else:
        return _reset_warn_count(chat_id=chat_id, user_id=user_id)

def check_warn_count(chat_id: int, user_id: int) -> int:
    if Config.USE_DATABASE:
        return database.check_warn_count(chat_id=chat_id, user_id=user_id)
    else:
        return _check_warn_count(chat_id=chat_id, user_id=user_id)
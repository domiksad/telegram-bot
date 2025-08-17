from typing import Dict, Tuple

# (chat_id, user_id) : warning count
warns_count: Dict[Tuple[int, int], int] = {}

def increment_warn_count(chat_id: int, user_id: int) -> int:
    key = (chat_id, user_id)
    if key not in warns_count:
        warns_count[key] = 1
    else:
        warns_count[key] += 1
    return warns_count[key] 

def decrement_warn_count(chat_id: int, user_id: int) -> int:
    key = (chat_id, user_id)
    if key not in warns_count:
        return -1
    elif warns_count[key] > 0:
        warns_count[key] -= 1
        return warns_count[key] 
    return -1

def reset_warn_count(chat_id: int, user_id: int):
    warns_count[(chat_id, user_id)] = 0

def check_warn_count(chat_id: int, user_id: int) -> int:
    return warns_count.get((chat_id, user_id), 0)
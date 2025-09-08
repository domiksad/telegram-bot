def get_next_key(d: dict, current: str) -> str:
    keys = list(d.keys())
    idx = keys.index(current)
    return keys[(idx + 1) % len(keys)]  # zawija się na początek

def get_prev_key(d: dict, current: str) -> str:
    keys = list(d.keys())
    idx = keys.index(current)
    return keys[(idx - 1) % len(keys)]  # zawija się na koniec
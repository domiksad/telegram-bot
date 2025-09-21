from tg_bot.modules.sql import con, cur
from tg_bot import LOGGER

# Optimization
groups_tracked = set()
def add_group(group_id: int):
    if group_id in groups_tracked: # group already tracked
        return
    
    cur.execute("INSERT OR IGNORE INTO groups VALUES (?)", [group_id])
    con.commit()

    groups_tracked.add(group_id)

def get_groups():
    cur.execute("SELECT chat_id from groups")
    rows = cur.fetchall()
    return [row["chat_id"] for row in rows]

from datetime import datetime, timezone

from telegram import ChatPermissions


''' 
{ (chat_id: int, user_id: int): {"previous_permissions": ChatPermissions, "until": datetime} }
'''
mutted_members = {}

def add_muted_member(chat_id: int, user_id: int, previous_permissions: ChatPermissions, until: datetime):
    mutted_members[(chat_id, user_id)] = {"previous_permissions": previous_permissions, "until": until}

def remove_muted_member(chat_id: int, user_id: int) -> ChatPermissions:
    previous_permissions = mutted_members[(chat_id, user_id)]["previous_permissions"]
    mutted_members.pop((chat_id, user_id), None)
    return previous_permissions
   
def update_muted_member_array():
    for key, value in list(mutted_members.items()):
        if value["until"] < datetime.now(timezone.utc):
            mutted_members.pop(key)
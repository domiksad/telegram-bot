from typing import Optional, Tuple
from datetime import datetime, timedelta, timezone


from telegram import ChatPermissions, Update, error, User, ChatMemberRestricted
from telegram.ext import ContextTypes

from tg_bot.config import Config
from tg_bot.modules.permissions import require_permission
from tg_bot.modules.user_info import get_target_user
from tg_bot.modules.muting import add_muted_member, remove_muted_member


"""Helper function for handlers"""
def moderation_action_factory(action: str):
    return lambda u, c: moderation_action(u, c, action)

@require_permission("can_restrict_members", "can_restrict_members")
async def moderation_action(update: Update, context: ContextTypes.DEFAULT_TYPE, moderation_action: str):
    result = await get_target_user(update=update, context=context)
    if result is None:
        await update.message.reply_text("No user specified or user not found")
        return 
    target_user, chat_member_status = result
    
    if chat_member_status == "administrator": 
        await update.message.reply_text(f"You can't {moderation_action} other admins")
        return
    elif chat_member_status == "creator":
        await update.message.reply_text(f"You can't {moderation_action} owner")
        return
    
    try:
        match moderation_action:
            case "kick":
                await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id)
                await context.bot.unban_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id)
                action_text = "kicked"
            case "ban":
                await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id)
                action_text = "banned"
            case "unban":
                await context.bot.unban_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id)
                action_text = "unbanned"
            case "mute": #### SPRAWDZIĆ CHATMEMBERRESTRICTED
                mute_time = datetime.now(timezone.utc) + timedelta(minutes=1) or Config.DEFAULT_MUTE_DURATION()
                if chat_member_status == "restricted":
                    chat_member = await context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id) # type: ChatMemberRestricted
                    perms = ChatPermissions(
                        can_send_messages=chat_member.can_send_messages,
                        can_send_media_messages=chat_member.can_send_media_messages,
                        can_send_polls=chat_member.can_send_polls,
                        can_send_other_messages=chat_member.can_send_other_messages,
                        can_add_web_page_previews=chat_member.can_add_web_page_previews,
                        can_change_info=chat_member.can_change_info,
                        can_invite_users=chat_member.can_invite_users,
                        can_pin_messages=chat_member.can_pin_messages,
                        can_manage_topics=getattr(chat_member, "can_manage_topics", False)
                    )
                else:
                    perms = (await context.bot.get_chat(update.effective_chat.id)).permissions # type: ChatPermissions
                
                await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id,
                    permissions=ChatPermissions(
                        can_send_messages=False,
                        can_send_other_messages=False,
                        can_add_web_page_previews=False,
                        can_change_info=False,
                        can_invite_users=False,
                        can_pin_messages=False
                    ), until_date=mute_time)
                add_muted_member(chat_id=update.effective_chat.id, user_id=target_user.id, previous_permissions=perms, until=mute_time)
                action_text = "muted"
            case "unmute":
                perms = remove_muted_member(chat_id=update.effective_chat.id, user_id=target_user.id) or (await context.bot.get_chat(update.effective_chat.id)).permissions
                await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id, permissions=perms)
                action_text = "unmuted"
            case "warn":
                action_text = "warned"
                pass
            case _:
                raise Exception(f"Wrong moderation_action {moderation_action}")
            
        await update.message.reply_text(f"User {target_user.name} was {action_text} by @{update.message.from_user.name}")
    except error.BadRequest as e:
        await update.message.reply_text(e.message)

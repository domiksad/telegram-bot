from typing import Optional, Tuple
from datetime import datetime, timedelta, timezone


from telegram import ChatPermissions, Update, error, ChatMemberRestricted
from telegram.ext import ContextTypes

from tg_bot.config import Config
from tg_bot.modules.permissions import require_permission, chat_member_to_permissions
from tg_bot.modules.user_info import get_target_user
from tg_bot.modules.warns import *


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
                reset_warn_count(chat_id=update.effective_chat.id, user_id=target_user.id)
                action_text = "unbanned"
            case "mute":
                mute_time = datetime.now(timezone.utc) + timedelta(minutes=1) or Config.DEFAULT_MUTE_DURATION()

                await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id,
                    permissions=ChatPermissions.no_permissions(),
                    until_date=mute_time)
                action_text = "muted"
            case "unmute":
                perms = (await context.bot.get_chat(update.effective_chat.id)).permissions # Default chat permissions

                await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id, permissions=perms)
                action_text = "unmuted"
            case "warn":
                target_user_warn_count = increment_warn_count(update.effective_chat.id, target_user.id)

                if target_user_warn_count >= Config.MAX_WARN_COUNT:
                    if Config.BAN_AFTER_REACHING_MAX_WARN_COUNT or Config.KICK_AFTER_REACHING_MAX_WARN_COUNT:
                        await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id)
                    if Config.KICK_AFTER_REACHING_MAX_WARN_COUNT: # user warn count is deleted after kicking
                        reset_warn_count(chat_id=update.effective_chat.id, user_id=target_user.id)
                        await context.bot.unban_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id)
                        await update.message.reply_text("User was kicked after reaching max warn count")
                    else:
                        await update.message.reply_text("User was banned after reaching max warn count")
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"[{target_user.full_name}](tg://user?id={target_user.id})\\. You have been warned {target_user_warn_count} time out of {Config.MAX_WARN_COUNT}", parse_mode="MarkdownV2")
                return 
                #  action_text = "warned"
            case "unwarn":
                target_user_warn_count = decrement_warn_count(update.effective_chat.id, target_user.id)
                if target_user_warn_count == -1:
                    await update.message.reply_text(f"User [{target_user.full_name}](tg://user?id={target_user.id}) hadnt any strikes", parse_mode="MarkdownV2")
                else:
                    await update.message.reply_text(f"Removed one strike from [{target_user.full_name}](tg://user?id={target_user.id})\\. Current count: {target_user_warn_count}", parse_mode="MarkdownV2")
                return
            case "check_user":
                target_user_warn_count = check_warn_count(update.effective_chat.id, target_user.id)
                await update.message.reply_text(f"User [{target_user.full_name}](tg://user?id={target_user.id})//, user_id: target_user.id//, strikes: {target_user_warn_count}/{Config.MAX_WARN_COUNT}", parse_mode="MarkdownV2")
            case _:
                raise Exception(f"Wrong moderation_action {moderation_action}")

        await update.message.reply_text(f"User [{target_user.full_name}](tg://user?id={target_user.id}) was {action_text} by [{update.message.from_user.full_name}](tg://user?id={update.message.from_user.id})", parse_mode="MarkdownV2")
    except error.BadRequest as e:
        await update.message.reply_text(e.message)

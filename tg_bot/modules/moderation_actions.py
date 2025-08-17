from datetime import datetime, timedelta, timezone

from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes

from tg_bot.config import Config
from tg_bot.modules.permissions import require_permission
from tg_bot.modules.user_info import get_target_user
from tg_bot.modules.warns import *
from tg_bot.modules.utils import mention_user_md


"""Returns target_user if everything is okay with target_user"""
async def validate_target(update: Update, context: ContextTypes.DEFAULT_TYPE, moderation_action: str):
    result = await get_target_user(update=update, context=context)
    if result is None:
        await update.message.reply_text("No user specified or user not found")
        return None
    target_user, chat_member_status = result

    if chat_member_status == "administrator": 
        await update.message.reply_text(f"You can't {moderation_action} other admins")
        return None
    if chat_member_status == "creator":
        await update.message.reply_text(f"You can't {moderation_action} owner")
        return None
    
    return target_user

@require_permission("can_restrict_members", "can_restrict_members")
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = await validate_target(update=update, context=context, moderation_action="kick")
    if not target_user: 
        return
    
    await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id)
    await context.bot.unban_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id)
    await update.message.reply_text(f"User [{target_user.full_name}](tg://user?id={target_user.id}) was kicked by [{update.message.from_user.full_name}](tg://user?id={update.message.from_user.id})", parse_mode="MarkdownV2")

@require_permission("can_restrict_members", "can_restrict_members")
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = await validate_target(update=update, context=context, moderation_action="ban")
    if not target_user:
        return
    
    await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id)
    await update.message.reply_text(f"User [{target_user.full_name}](tg://user?id={target_user.id}) was banned by [{update.message.from_user.full_name}](tg://user?id={update.message.from_user.id})", parse_mode="MarkdownV2")

@require_permission("can_restrict_members", "can_restrict_members")
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = await validate_target(update=update, context=context, moderation_action="unban")
    if not target_user:
        return

    if Config.RESET_WARN_COUNT_AFTER_UNBANNING:
        reset_warn_count(chat_id=update.effective_chat.id, user_id=target_user.id)
    await context.bot.unban_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id)
    await update.message.reply_text(f"User [{target_user.full_name}](tg://user?id={target_user.id}) was unbanned by [{update.message.from_user.full_name}](tg://user?id={update.message.from_user.id})", parse_mode="MarkdownV2")

@require_permission("can_restrict_members", "can_restrict_members")
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = await validate_target(update=update, context=context, moderation_action="mute")
    if not target_user:
        return
    
    mute_time = datetime.now(timezone.utc) + timedelta(minutes=1) or Config.DEFAULT_MUTE_DURATION()

    await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id, permissions=ChatPermissions.no_permissions(), until_date=mute_time)
    await update.message.reply_text(f"User [{target_user.full_name}](tg://user?id={target_user.id}) was muted by [{update.message.from_user.full_name}](tg://user?id={update.message.from_user.id})", parse_mode="MarkdownV2")

@require_permission("can_restrict_members", "can_restrict_members")
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = await validate_target(update=update, context=context, moderation_action="unmute")
    if not target_user:
        return
    
    perms = (await context.bot.get_chat(update.effective_chat.id)).permissions # Default chat permissions
    await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id, permissions=perms)
    await update.message.reply_text(f"User [{target_user.full_name}](tg://user?id={target_user.id}) was unmuted by [{update.message.from_user.full_name}](tg://user?id={update.message.from_user.id})", parse_mode="MarkdownV2")

@require_permission("can_restrict_members", "can_restrict_members")
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = await validate_target(update=update, context=context, moderation_action="warn")
    if not target_user:
        return
    
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

@require_permission("can_restrict_members", "can_restrict_members")
async def unwarn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = await validate_target(update=update, context=context, moderation_action="unwarn")
    if not target_user:
        return
    
    target_user_warn_count = decrement_warn_count(update.effective_chat.id, target_user.id)
    if target_user_warn_count == -1:
        await update.message.reply_text(f"User [{target_user.full_name}](tg://user?id={target_user.id}) hadnt any strikes", parse_mode="MarkdownV2")
    else:
        await update.message.reply_text(f"Removed one strike from [{target_user.full_name}](tg://user?id={target_user.id})\\. Current count: {target_user_warn_count}", parse_mode="MarkdownV2")

@require_permission("can_restrict_members", "can_restrict_members")
async def check_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = await get_target_user(update=update, context=context)
    if not result:
        await update.message.reply_text("Usage: /check_user [mention | by reply]")
        return
    target_user = result[0]

    target_user_warn_count = check_warn_count(update.effective_chat.id, target_user.id)
    await update.message.reply_text(f"User {mention_user_md(target_user)}, user\\_id: {target_user.id}, strikes: {target_user_warn_count}/{Config.MAX_WARN_COUNT}", parse_mode="MarkdownV2")

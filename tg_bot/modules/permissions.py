from functools import wraps

from telegram import Update, Bot, ChatMemberMember, ChatMemberAdministrator, ChatMemberRestricted, ChatPermissions
from telegram.ext import ContextTypes


"""DECORATORS"""
def require_permission(user_permission, bot_permission=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            user_id = update.effective_user.id
            chat_id = update.effective_chat.id
            user_member = await context.bot.get_chat_member(chat_id, user_id)

            if user_member.status == "creator":
                pass
            elif isinstance(user_member, ChatMemberAdministrator):
                if getattr(user_member, user_permission, False):
                    return await func(update, context, *args, **kwargs)
                else:
                    await update.message.reply_text(f'You need "{user_permission.replace('_', ' ')}" permission to use this command')
                    return
            else:
                await update.message.reply_text("You must be an admin to use this command")
                return
            
            if not bot_permission:
                return await func(update, context, *args, **kwargs)
            
            bot_member = await context.bot.get_chat_member(chat_id=chat_id, user_id=context.bot.id)
            if isinstance(bot_member, ChatMemberAdministrator):
                if bot_permission and not getattr(bot_member, bot_permission):
                    await update.message.reply_text(f'I need "{user_permission.replace('_', ' ')}" permission to perform this action')
                    return
            else:
                await update.message.reply_text("I am not an admin in this group")

            return await func(update, context, *args, **kwargs)
        return wrapper
    return decorator

def require_admin(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id

        member = await context.bot.get_chat_member(chat_id, user_id)

        if member.status in ["administrator", "creator"]:
            return await func(update, context, *args, **kwargs)
        else:
            await update.message.reply_text("Only admins can use this command")
    return wrapper


"""FUNCTIONS"""


@require_admin
async def check_bot_permissions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    bot_id = context.bot.id
    bot_member = await context.bot.get_chat_member(chat.id, bot_id)

    if(isinstance(bot_member, ChatMemberAdministrator)):
        await update.message.reply_text(f'The bot has the following permissions:\nCan delete messages: {bot_member.can_delete_messages}\nCan pin messages: {bot_member.can_pin_messages}\nCan restrict members: {bot_member.can_restrict_members}')
        return
    elif isinstance(bot_member, ChatMemberMember):
        await update.message.reply_text("The bot is regular member and cannot help with moderation")
        return
    else:
        await update.message.reply_text(f"Bot status: {bot_member.status}")
        return


def chat_member_to_permissions(chat_member: ChatMemberRestricted):
    return ChatPermissions(
        can_send_messages=chat_member.can_send_messages,
        can_send_audios=chat_member.can_send_audios,
        can_send_documents=chat_member.can_send_documents,
        can_send_photos=chat_member.can_send_photos,
        can_send_videos=chat_member.can_send_videos,
        can_send_video_notes=chat_member.can_send_video_notes,
        can_send_voice_notes=chat_member.can_send_voice_notes,
        can_send_polls=chat_member.can_send_polls,
        can_send_other_messages=chat_member.can_send_other_messages,
        can_add_web_page_previews=chat_member.can_add_web_page_previews,
        can_change_info=chat_member.can_change_info,
        can_invite_users=chat_member.can_invite_users,
        can_pin_messages=chat_member.can_pin_messages,
        can_manage_topics=chat_member.can_manage_topics
    )

@require_admin
async def check_member_permissions(update: Update, context: ContextTypes.DEFAULT_TYPE): # will only work with replies bc
    chat_member = await context.bot.get_chat_member(update.effective_chat.id, update.message.reply_to_message.from_user.id)

    if chat_member.status != "restricted":
        await update.message.reply_text(f"User is {chat_member.status}. He has default permissions")
        return
    
    attrs = [
        "can_send_messages", "can_send_audios", "can_send_documents", "can_send_photos",
        "can_send_videos", "can_send_video_notes", "can_send_voice_notes", "can_send_polls",
        "can_send_other_messages", "can_add_web_page_previews", "can_change_info",
        "can_invite_users", "can_pin_messages", "can_manage_topics"
    ]
    message = "=== Perms ===\n"
    for attr in attrs:
        message += f"{attr}: {getattr(chat_member, attr, None)}\n"
    message += "=== EOF Perms ==="
    await update.message.reply_text(message)

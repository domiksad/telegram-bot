import logging
from datetime import datetime, timedelta, timezone
from dotenv import dotenv_values # for token
from functools import wraps # admin validation
from collections import deque # chat history
from telegram import ChatPermissions, Update, ChatMemberAdministrator, ChatMemberMember, error
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from profanityfilter import ProfanityFilter

TOKEN = dotenv_values(".env")["TOKEN"]

# profanity filter settings
use_profanity_filter = True
pf = ProfanityFilter()
notify_about_profanity = True; profanity_notification_text = "You said profane thing. Stop it"

# moderation actions settings 
DEFAULT_MUTE_DURATION = lambda: datetime.now(timezone.utc) + timedelta(days=3)

# permissions
# has_permissions = [] # chat_id: [perms...]
# permissionSuccessfulNotif = "I have all perms needed"
# noPermissionNotif = "I dont have perms :/"

# rules
rules_text = "1. Do not swear\n2. No erp you kinky piece of shit"

# internal logic settings
# DEQUE_MAX_LEN = 1_000

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# some shit - internal logic

# { (chat_id: int, user_id: int): {"previous_permissions": ChatPermissions, "until": datetime} }
mutted_members = {}

def add_muted_member(chat_id: int, user_id: int, previous_permissions: ChatPermissions, until: datetime):
    mutted_members[(chat_id, user_id)] = {"previous_permissions": previous_permissions, "until": until}

def remove_muted_member(chat_id: int, user_id: int):
    previous_permissions = mutted_members[(chat_id, user_id)]["previous_permissions"]
    mutted_members.pop((chat_id, user_id), None)
    return previous_permissions
   
def update_muted_member_array():
    for key, value in list(mutted_members.items()):
        if value["until"] < datetime.now(timezone.utc):
            mutted_members.pop(key)

async def profanity_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message or update.edited_message
    if not message or not message.text:
        return
    text = message.text
    if(pf.is_profane(text) & notify_about_profanity):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=profanity_notification_text, reply_to_message_id=update.message.message_id)

def require_permission(user_permission, bot_permission=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(update, context, *args, **kwargs):
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
            
            bot_id = context.bot.id
            bot_member = await context.bot.get_chat_member(chat_id, bot_id)
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
    async def wrapper(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id

        member = await context.bot.get_chat_member(chat_id, user_id)

        if member.status in ["administrator", "creator"]:
            return await func(update, context, *args, **kwargs)
        else:
            await update.message.reply_text("Only admins can use this command")
    return wrapper

async def get_target_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = None

    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user

    elif context.args:
        arg = context.args[0]
        try:
            user_id = int(arg)
            chat_member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
            target_user = chat_member.user
        except ValueError:
            for entity in update.message.entities or []:
                if entity.type == "text_mention":
                    target_user = entity.user
                    break
                # elif entity.type == "mention":
                #     username = update.message.text[entity.offset+1 : entity.offset+entity.length]
                #     try:
                #         target_user = await context.bot.get_chat(username)
                #     except:
                        # return None

    if not target_user:
        return None

    chat_member = await context.bot.get_chat_member(update.effective_chat.id, target_user.id)
    return [target_user, chat_member.status]
# end of internal logic

# commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    return await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

# admin commands start

@require_admin
async def check_permissions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    bot_id = context.bot.id
    bot_member = await context.bot.get_chat_member(chat.id, bot_id)

    if(isinstance(bot_member, ChatMemberAdministrator)):
        return await update.message.reply_text(f'The bot has the following permissions:\nCan delete messages: {bot_member.can_delete_messages}\nCan pin messages: {bot_member.can_pin_messages}\nCan restrict members: {bot_member.can_restrict_members}')
    elif isinstance(bot_member, ChatMemberMember):
        return await update.message.reply_text("The bot is regular member and cannot help with moderation")
    else:
        return await update.message.reply_text(f"Bot status: {bot_member.status}")



@require_permission("can_restrict_members", "can_restrict_members")
async def moderation_action(update: Update, context: ContextTypes.DEFAULT_TYPE, moderation_action: str):
    result = await get_target_user(update=update, context=context)
    if result is None:
        return await update.message.reply_text("No user specified or user not found")
    target_user, chat_member_status = result

    if chat_member_status == "administrator": 
        return await update.message.reply_text(f"You can't {moderation_action} other admins")
    elif chat_member_status == "creator":
        return await update.message.reply_text(f"You can't {moderation_action} owner")

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
            case "mute":
                mute_time = datetime.now(timezone.utc) + timedelta(minutes=1)
                # complicated logic
                if hasattr(target_user, "permissions") and target_user.permissions:
                    perms = target_user.permissions
                else:
                    perms = (await context.bot.get_chat(update.effective_chat.id)).permissions
                
                await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id,
                    permissions=ChatPermissions(
                        can_send_messages=False,
                        can_send_other_messages=False,
                        can_add_web_page_previews=False,
                        can_change_info=False,
                        can_invite_users=False,
                        can_pin_messages=False
                    ), until_date=mute_time or DEFAULT_MUTE_DURATION)
                add_muted_member(chat_id=update.effective_chat.id, user_id=target_user.id, previous_permissions=perms, until=mute_time or DEFAULT_MUTE_DURATION)
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

# admin commands stop

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    # commands
    start_handler = CommandHandler('start', start); application.add_handler(start_handler)

    # admin commands
    check_permissions_handler  = CommandHandler('check_permissions', check_permissions);                                                        application.add_handler(check_permissions_handler)
    kick_handler               = CommandHandler('kick', lambda u, c: moderation_action(u, c, "kick"), filters=filters.UpdateType.MESSAGE);      application.add_handler(kick_handler)
    ban_handler                = CommandHandler('ban', lambda u, c: moderation_action(u, c, "ban"), filters=filters.UpdateType.MESSAGE);        application.add_handler(ban_handler)
    warn_handler               = CommandHandler('warn', lambda u, c: moderation_action(u, c, "warn"), filters=filters.UpdateType.MESSAGE);      application.add_handler(warn_handler)
    mute_handler               = CommandHandler('mute', lambda u, c: moderation_action(u, c, "mute"), filters=filters.UpdateType.MESSAGE);      application.add_handler(mute_handler)
    unmute_handler             = CommandHandler('unmute', lambda u, c: moderation_action(u, c, "unmute"), filters=filters.UpdateType.MESSAGE); application.add_handler(unmute_handler)
    unban_handler              = CommandHandler('unban', lambda u, c: moderation_action(u, c, "unban"), filters=filters.UpdateType.MESSAGE);    application.add_handler(unban_handler)

    # censorship
    messages_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), profanity_filter); application.add_handler(messages_handler) # its decorator now

    application.run_polling()
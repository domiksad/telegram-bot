import logging
from dotenv import dotenv_values # for token
from functools import wraps # admin validation
from collections import deque # chat history
from telegram import Update, ChatMemberAdministrator, ChatMemberMember, error
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from profanityfilter import ProfanityFilter

TOKEN = dotenv_values(".env")["TOKEN"]

# profanity filter settings
use_profanity_filter = True
pf = ProfanityFilter()
notify_about_profanity = True; profanity_notification_text = "You said profane thing. Stop it"

# permissions
# has_permissions = [] # chat_id: [perms...]
# permissionSuccessfulNotif = "I have all perms needed"
# noPermissionNotif = "I dont have perms :/"

# rules
rules_text = "1. Do not swear\n2. No erp you kinky piece of shit"

# internal logic settings
DEQUE_MAX_LEN = 1_000

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# some shit - internal logic
# chat history start
message_cache = deque(maxlen=DEQUE_MAX_LEN) # {"id": ..., "user_id": ...}

def add_message(id, user_id):
    message_cache.append({id, user_id})

# chat history stop

async def handle_new_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message: # if its new message
        message_id = update.message.id
        add_message(message_id, update.message.from_user.id) # then add it to deque
    elif update.edited_message: # if its edited message
        message_id = update.edited_message.id
        if not message_cache[update.edited_message]: # check if it is in stack
            add_message(update.edited_message.id, update.edited_message.from_user.id) # if not then add it

    if not use_profanity_filter:
        return
    
    message = update.message or update.edited_message
    text = message.text
    if(pf.is_profane(text) & notify_about_profanity):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=profanity_notification_text, reply_to_message_id=message_id)

# async def profanity_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     message = update.message or update.edited_message
#     if not message or not message.text:
#         return
#     text = message.text
#     if(pf.is_profane(text) & notify_about_profanity):
#         await context.bot.send_message(chat_id=update.effective_chat.id, text=profanity_notification_text, reply_to_message_id=update.message.message_id)

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

@require_permission("can_delete_messages", "can_delete_messages")
async def purge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("Reply to a message to start purging from.")
    
    try:
        amount = int(context.args[0])
    except (IndexError, ValueError):
        return await update.message.reply_text("Usage: /purge <number_of_messages>")
    
    chat_id = update.effective_chat.id
    start_msg_id = update.message.reply_to_message.id
    current_id = start_msg_id
    deleted = 0
    max_failures = 10
    failures = 0

    while deleted < amount and current_id > 0 and current_id != start_msg_id:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=current_id)
            deleted += 1
            failures = 0 
        except error.BadRequest as e:
            if "message to delete not found" in str(e).lower():
                failures += 1
                if failures >= max_failures:
                    break
            else:
                raise
        current_id += 1
    return await update.message.reply_text(f"Deleted {deleted} messages")

@require_permission("can_restrict_members", "can_restrict_members")
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Can kick people")

@require_permission("can_restrict_members", "can_restrict_members")
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Can ban people")

@require_permission("can_restrict_members", "can_restrict_members")
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Can warn people")

@require_permission("can_restrict_members", "can_restrict_members")
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Can mute people")

# admin commands stop

# debug commands start
async def show_message_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("working")
    await update.message.reply_text("history: \n" + message_cache)
# debug commands stop

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    # commands
    start_handler = CommandHandler('start', start); application.add_handler(start_handler)

    # admin commands
    check_permissions_handler = CommandHandler('check_permissions', check_permissions); application.add_handler(check_permissions_handler)
    kick_handler              = CommandHandler('kick', kick);                           application.add_handler(kick_handler)
    ban_handler               = CommandHandler('ban', ban);                             application.add_handler(ban_handler)
    warn_handler              = CommandHandler('warn', warn);                           application.add_handler(warn_handler)
    mute_handler              = CommandHandler('mute', mute);                           application.add_handler(mute_handler)
    purge_handler             = CommandHandler('purge', purge);                         application.add_handler(purge_handler)

    # censorship
    messages_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_new_message); application.add_handler(messages_handler)

    # debug
    show_message_history_handler = CommandHandler('show_message_history', show_message_history); application.add_handler(show_message_history_handler)

    application.run_polling()
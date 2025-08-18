from telegram import Update, User
from telegram.ext import ContextTypes

from tg_bot.modules.database import set_welcome_message_db, read_welcome_message_db
from tg_bot.modules.permissions import require_admin
from tg_bot.modules.utils import mention_user_md
from tg_bot.config import Config

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from tg_bot.modules.commands import COMMANDS # fix circular import error
    await update.message.reply_text("Commands:\n"+"\n".join(COMMANDS.keys()))



rules_array = {} # chat_id: rule
def _set_welcome_message_array(chat_id: int, text: str):
    rules_array[chat_id] = text

def _read_welcome_message_array(chat_id: int):
    if rules_array[chat_id]:
        return rules_array[chat_id]
    return None

# replace_tags = {
#     "[user]": lambda u, c: u.mention_markdown_v2(),
#     "[channel_name]": lambda u, c: c.title or "this chat"
# }

@require_admin
async def set_welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.edited_message:
        await update.message.reply_text("Usage: /set_welcome_message [text]")
        return

    args = context.args
    if not args:
        await update.message.reply_text("Usage: /set_welcome_message [text]")
        return
    
    message_text = " ".join(args)
    if Config.USE_DATABASE:
        set_welcome_message_db(chat_id=update.effective_chat.id,welcome_message_text=message_text)
    else:
        _set_welcome_message_array(chat_id=update.effective_chat.id,text=message_text)
    await update.message.reply_text("New welcome message set")

async def read_welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if Config.USE_DATABASE:
        welcome_message = read_welcome_message_db(update.effective_chat.id)
    else:
        welcome_message = _read_welcome_message_array(chat_id=update.effective_chat.id)
    
    if not welcome_message:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No welcome message set.")
        return

    # for tag, func in replace_tags.items():
    #     if tag in welcome_message:
    #         welcome_message = welcome_message.replace(tag, func(update.effective_user, update.effective_chat))

    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message) #, parse_mode="MarkdownV2")
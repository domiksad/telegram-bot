from telegram import Update
from telegram.ext import ContextTypes

from tg_bot.modules import database
from tg_bot.config import Config
from tg_bot.modules.permissions import require_admin


rules_tuple = {}
def _add_rule_tuple(chat_id: int, rule: str):
    rules_tuple[chat_id] = rule

def _read_rule_tuple(chat_id: int):
    rule = rules_tuple.get(chat_id)
    if not rule:
        return ""
    return rule

###
@require_admin
async def add_rule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /set_rule [text]")
        return
    user_input = " ".join(args)

    if Config.USE_DATABASE:
        database.add_rule_db(chat_id=update.effective_chat.id, rule=user_input)
    else:
        _add_rule_tuple(chat_id=update.effective_chat.id, rule=user_input)

    await update.message.reply_text("New rule was set")

async def read_rule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if Config.USE_DATABASE:
        rule = database.read_rule_db(chat_id=update.effective_chat.id)
    else:
        rule = _read_rule_tuple(chat_id=update.effective_chat.id)
    
    if not rule:
        await update.message.reply_text("No rules set yet")
        return 
        
    await update.message.reply_text(rule)
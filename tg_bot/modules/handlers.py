from telegram.ext import filters, MessageHandler, Application, CommandHandler
from tg_bot.modules.profanity_filter import profanity_filter_function
from tg_bot.modules.commands import COMMANDS, FILTERS
from tg_bot.modules.intro import read_welcome_message

def register_handlers(application: Application):
    """Registers nearly all commands"""
    for cmd, func in COMMANDS.items():
        f = FILTERS.get(cmd)
        application.add_handler(CommandHandler(cmd, func, filters=f))

def register_profanity_filter(application: Application):
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), profanity_filter_function))

def welcome_message_filter(application: Application):
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, read_welcome_message))
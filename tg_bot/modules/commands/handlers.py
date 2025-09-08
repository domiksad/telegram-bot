from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from tg_bot.modules.commands.commands import COMMANDS, FILTERS, button_handler


def register_button_handler(application: Application) -> None:
    application.add_handler(CallbackQueryHandler(button_handler))

def register_handlers(application: Application) -> None:
    """Registers commands"""
    for cmd, func in COMMANDS.items():
        f = FILTERS.get(cmd)
        application.add_handler(CommandHandler(cmd, func, filters=f))

    register_button_handler(application=application)
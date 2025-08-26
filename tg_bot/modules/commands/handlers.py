from telegram.ext import Application, CommandHandler

from tg_bot.modules.commands.commands import COMMANDS, FILTERS


def register_handlers(application: Application) -> None:
    """Registers commands"""
    for cmd, func in COMMANDS.items():
        f = FILTERS.get(cmd)
        application.add_handler(CommandHandler(cmd, func, filters=f))
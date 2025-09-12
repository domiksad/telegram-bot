from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from tg_bot.modules.commands.commands import COMMANDS, FILTERS, button_handler, dm_handle_message, welcome_user


###                         dont forget to add register to register_handlers                         ###

def register_button_handler(application: Application) -> None:
    application.add_handler(CallbackQueryHandler(button_handler))

def register_dm_message_handler(application: Application) -> None:
    application.add_handler(MessageHandler((filters.TEXT | filters.PHOTO | filters.ANIMATION | filters.Sticker.ALL) & filters.ChatType.PRIVATE, dm_handle_message))

def register_welcome_user(application: Application) -> None:
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_user))

def register_handlers(application: Application) -> None:
    """Registers commands"""
    for cmd, func in COMMANDS.items():
        f = FILTERS.get(cmd)
        application.add_handler(CommandHandler(cmd, func, filters=f))

    register_button_handler(application=application)
    register_dm_message_handler(application=application)
    register_welcome_user(application=application)
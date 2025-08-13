from profanityfilter import ProfanityFilter

from telegram.ext import filters, MessageHandler, Application, CommandHandler

from tg_bot.modules.moderation_actions import moderation_action_factory
from tg_bot.modules.start import start
from tg_bot.modules.permissions import check_bot_permissions
from tg_bot.modules.profanity_filter import make_profanity_filter_handler


def register_handlers(application: Application):
    """Registers nearly all commands"""
    commands = {
        "start": start,
        "check_permissions": check_bot_permissions,
        "kick": moderation_action_factory("kick"),
        "ban": moderation_action_factory("ban"),
        "warn": moderation_action_factory("warn"),
        "mute": moderation_action_factory("mute"),
        "unmute": moderation_action_factory("unmute"),
        "unban": moderation_action_factory("unban"),
    }

    for cmd, func in commands.items():
        f = filters.UpdateType.MESSAGE if cmd in {"kick", "ban", "warn", "mute", "unmute", "unban"} else None
        application.add_handler(CommandHandler(cmd, func, filters=f))

def register_profanity_filter(application: Application, profanity_filter_instance: ProfanityFilter):
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), make_profanity_filter_handler(profanity_filter_instance)))

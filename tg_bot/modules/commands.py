from telegram.ext import filters

from tg_bot.modules.moderation_actions import check_user, kick, ban, unban, warn, unwarn, mute, unmute
from tg_bot.modules.intro import start, help, set_welcome_message
from tg_bot.modules.permissions import check_bot_permissions, check_member_permissions
from tg_bot.modules.rules import add_rule, read_rule 


COMMANDS = {
    "start": start,
    "check_permissions": check_bot_permissions,
    "check_user_permissions": check_member_permissions,
    "check_user": check_user,
    "kick": kick,
    "ban": ban,
    "unban": unban,
    "warn": warn,
    "unwarn": unwarn,
    "mute": mute,
    "unmute": unmute,
    "help": help,
    "set_rule": add_rule,
    "rules": read_rule,
    "set_welcome_message": set_welcome_message
}

FILTERS = {
    "kick": filters.UpdateType.MESSAGE,
    "ban": filters.UpdateType.MESSAGE, 
    "warn": filters.UpdateType.MESSAGE, 
    "mute": filters.UpdateType.MESSAGE, 
    "unmute": filters.UpdateType.MESSAGE, 
    "unban": filters.UpdateType.MESSAGE
}

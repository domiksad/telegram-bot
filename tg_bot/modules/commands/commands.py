from tg_bot.modules.moderation_actions.kick import kick
from tg_bot.modules.moderation_actions.ban import ban, unban
from tg_bot.modules.moderation_actions.mute import mute, unmute
from tg_bot.modules.moderation_actions.warn import warn, unwarn
from tg_bot.modules.misc_actions.help import help
from tg_bot.modules.channel_settings.settings import get_settings_panel, button_handler, dm_handle_message
from tg_bot.modules.misc_actions.welcome import welcome_user # <- do not delete. Used in handlers ^^^

COMMANDS = {
    "kick": kick,
    "ban": ban,
    "unban": unban,
    "mute": mute,
    "unmute": unmute,
    "warn": warn,
    "unwarn": unwarn,
    "settings": get_settings_panel,
    "help": help,
}

FILTERS = {
    
}
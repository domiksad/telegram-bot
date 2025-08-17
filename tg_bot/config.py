import os
from profanityfilter import ProfanityFilter
from datetime import datetime, timedelta, timezone


class Config:
    # Bot token
    API_KEY = None # type: str

    # Profanity filter
    pf = ProfanityFilter()
    USE_PROFANITY_FILTER = True
    NOTIFY_ABOUT_PROFANITY = True
    PROFANITY_NOTIFICATION_TEXT = "You said profane thing. Stop it"

    # Moderation
    DEFAULT_MUTE_DURATION_DAYS = 3
    DEFAULT_MUTE_DURATION_HOURS = 0
    DEFAULT_MUTE_DURATION_MINUTES = 0

    MAX_WARN_COUNT = 3
    KICK_AFTER_REACHING_MAX_WARN_COUNT = True
    BAN_AFTER_REACHING_MAX_WARN_COUNT = False
    BAN_WARN_DURATION_DAYS = 0 # 0 means ban until someone unbans him. MAX 365 days
    RESET_WARN_COUNT_AFTER_UNBANNING = True

    # Database settings
    USE_DATABASE = True # Changing it may cause errors
    DATABASE_NAME = "main"

    # Other
    RULES_TEXT = "1. Do not swear\n2. No erp you kinky piece of shit"

    # Computed values
    @staticmethod
    def DEFAULT_MUTE_DURATION():
        return datetime.now(timezone.utc) + timedelta(
            days=Config.DEFAULT_MUTE_DURATION_DAYS,
            hours=Config.DEFAULT_MUTE_DURATION_HOURS,
            minutes=Config.DEFAULT_MUTE_DURATION_MINUTES
        )
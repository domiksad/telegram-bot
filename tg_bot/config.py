import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv 

load_dotenv()

class Config:
    # Bot token
    API_KEY = os.getenv("TOKEN")

    # Profanity filter
    USE_PROFANITY_FILTER = True
    NOTIFY_ABOUT_PROFANITY = True
    PROFANITY_NOTIFICATION_TEXT = "You said profane thing. Stop it"

    # Moderation
    DEFAULT_MUTE_DURATION_DAYS = 3
    DEFAULT_MUTE_DURATION_HOURS = 0
    DEFAULT_MUTE_DURATION_MINUTES = 0

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
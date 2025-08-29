from tg_bot.modules.sql.settings import get_chat_language

def get_dialog(key: str, chat_id: int = None, lang: str = None) -> str: # type: ignore
    if lang is None:
        if chat_id is None:
            raise ValueError("Either lang or chat_id must be provided")
        lang = get_chat_language(chat_id=chat_id)
    return LANG[lang].get(key) or key

LANG = {
    "pl": {
        "BOT_IS_NOT_AN_ADMIN": "Bot nie jest adminem",
        "USER_IS_NOT_AN_ADMIN": "Nie jesteś adminem",
        "BOT_CANT_RESTRICT": "Bot nie może ograniczać w tym kanale",
        "USER_CANT_RESTRICT": "Użytkownik nie może ograniczać w tym kanale",
        "NO_USER_TARGET": "Musisz wskazać użytkownika poprzez odpowiedź, podanie ID lub wzmiankę",
        "CANT_RESTRICT_ADMINS": "Nie mogę ograniczać innych administratorów",
        "CANT_RESTRICT_MYSELF": "Nie mogę sam siebie ograniczyć",
        "WHY_UNBAN_USER_ALREADY_IN_CHAT": "Użytkownik jest już na czacie więc nie trzeba go odbanowywać",
        "SPECIFY_TIME": "Musisz podać czas, np. 5m, 2h, 1d.",
        "INVALID_TIME": "Nieprawidłowy format czasu. Użyj np.: 5m, 2h, 1d lub 2d3h15m.",
        "TIME_GREATER_THAN_ZERO": "Czas musi być większy niż 0.",
        "USER_NOT_IN_CHAT": "{user} nie ma na czacie",
        "KICKED": "{user} został wyrzucony. Powód: {reason}",
        "BANNED": "{user} został zbanowany",
        "UNBANNED": "{user} został odbanowany",
        "MUTED": "{user} został wyciszony na {until_date}",
        "UNMUTED": "{user} może już pisać",
        "USER_ISNT_MUTED": "{user} nie jest wyciszony",
        "WARNED": "{user} został ostrzeżony {warn_count}/{max_warn_count}",
        "WARN_BANNED": "{user} został zbanowany po przekroczeniu limitu ostrzeżeń",
        "WARN_KICKED": "{user} został wyrzucony po przekroczeniu limitu ostrzeżeń",
        "UNWARNED": "{user} usunięto ostrzeżenie {warn_count}/{max_warn_count}",
        "NO_REASON_PROVIDED": "Brak powodu",
    },
    "eng": {
        "SPECIFY_TIME": "You need to specify a time, e.g. 5m, 2h, 1d.",
        "INVALID_TIME": "Invalid time format. Use something like: 5m, 2h, 1d or 2d3h15m.",
        "TIME_GREATER_THAN_ZERO": "Time must be greater than 0.",
        "MUTED": "{user} has been muted for {until_date}",
    }
}
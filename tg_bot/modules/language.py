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
        "USER_NOT_IN_CHAT": "Użytkownika nie ma na czacie",
        "KICKED": "{user} został wyrzucony. Powód: {reason}",
        "BANNED": "{user} został zbanowany. Powód: {reason}",
        "UNBANNED": "{user} został odbanowany",
        "MUTED": "{user} został wyciszony na {until_date}. Powód: {reason}",
        "UNMUTED": "{user} może już pisać",
        "USER_ISNT_MUTED": "{user} nie jest wyciszony",
        "WARNED": "{user} został ostrzeżony {warn_count}/{max_warn_count}. Powód: {reason}",
        "WARN_BANNED": "{user} został zbanowany po przekroczeniu limitu ostrzeżeń. Powód: {reason}",
        "WARN_KICKED": "{user} został wyrzucony po przekroczeniu limitu ostrzeżeń. Powód: {reason}",
        "UNWARNED": "{user} usunięto ostrzeżenie {warn_count}/{max_warn_count}",
        "NO_REASON_PROVIDED": "Brak powodu",
        "CREATOR_ONLY": "Tylko twórca czatu może użyć tej komendy",
        "SENT_IN_DM": "Wysłałem na czacie prywatnym",
        "CANT_USE_COMMAND_IN_DMS": "Nie możesz użyć tej komendy w wiadomościach prywatnych",
        "COMMANDS": "Komendy:",
        "NO_PERMISSIONS_TO_CHANGE_SETTINGS": "Nie masz uprawnień do zmiany ustawień tej grupy",
        "START_DM_WITH_BOT": "Napisz najpierw do mnie",
        "USAGE": "Użycie: {command} {args}",
        "SETTINGS_PANEL": "Panel ustawień dla {id}",
        "SOFT_WARN_INFO": "Gdy soft_warn jest off, po osiągnięciu maks. ostrzeżeń zostajesz zablokowany; gdy on, zostajesz wyrzucony",
        "UNSUPPORTED_MESSAGE_TYPE": "Nieobsługiwany typ wiadomości dla oczekiwanego typu {msg_type}",
        "WELCOME_MESSAGE_SET": "Wiadomość powitalna ustawiona. Będę wyświetlał:",
        "INPUT_EXPIRED": "Czas na wprowadzenie danych minął",
        "SEND_NEW_WELCOME_MESSAGE": "Wyślij nową treść wiadomości powitalnej",
        "CURRENT_MEDIA": "Obecnie ustawiona wiadomość/media",
        "SELECT_GROUP": "Wybierz grupę do konfigurowania",
    },
    "eng": {
        "SPECIFY_TIME": "You need to specify a time, e.g. 5m, 2h, 1d.",
        "INVALID_TIME": "Invalid time format. Use something like: 5m, 2h, 1d or 2d3h15m.",
        "TIME_GREATER_THAN_ZERO": "Time must be greater than 0.",
        "MUTED": "{user} has been muted for {until_date}",
        "UNSUPPORTED_MESSAGE_TYPE": "Unsupported message type for expected type '{msg_type}'",
        "WELCOME_MESSAGE_SET": "Welcome message updated! Will display:",
        "INPUT_EXPIRED": "Your input expired",
        "SEND_NEW_WELCOME_MESSAGE": "Please send the new content for the welcome message",
        "SELECT_GROUP": "Select group to configure",
        "CURRENT_MEDIA": "Currently set message/media",
    }
}
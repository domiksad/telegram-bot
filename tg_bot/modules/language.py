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
    }
}
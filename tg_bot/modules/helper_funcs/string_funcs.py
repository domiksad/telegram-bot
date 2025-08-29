import html

from telegram import User

def html_mention(user: User) -> str: # fix it in future for injections
    return f'<a href="tg://user?id={user.id}">{user.first_name}</a>'

def escape_html(text: str) -> str:
    return html.escape(text)
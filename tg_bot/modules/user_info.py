from typing import Optional, Tuple

from telegram import Update, User
from telegram.ext import ContextTypes

async def get_target_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Optional[Tuple[User, str]]:
    target_user = None # type: Optional[User]

    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user

    elif context.args:
        arg = context.args[0]
        try:
            user_id = int(arg)
            chat_member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
            target_user = chat_member.user
        except ValueError:
            for entity in update.message.entities or []:
                if entity.type == "text_mention":
                    target_user = entity.user
                    break
                # elif entity.type == "mention":
                #     username = update.message.text[entity.offset+1 : entity.offset+entity.length]
                #     try:
                #         target_user = await context.bot.get_chat(username)
                #     except:
                        # return None

    if not target_user:
        return None
    
    chat_member = await context.bot.get_chat_member(update.effective_chat.id, target_user.id)
    return [target_user, chat_member.status]
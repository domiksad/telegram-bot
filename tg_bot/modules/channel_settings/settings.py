from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, CallbackQuery, error
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from tg_bot.modules.sql.settings import * 
from tg_bot.modules.helper_funcs.chat_status import bot_admin, user_admin
from tg_bot.modules.helper_funcs.array_funcs import get_next_key, get_prev_key
from tg_bot.modules.language import get_dialog, LANG
from tg_bot import LOGGER


TEXTS = ["❌ Off", "✅ On"] # False (0); True (1)

def build_keyboard(chat_id: int, settings: dict) -> InlineKeyboardMarkup:
    LOGGER.info(f"BUILING KEYBOARD. Settings: {settings.items()}")
    keyboard = [ # callback can have max 64 chars
        [
            InlineKeyboardButton("⬅️", callback_data=f"lang_dec:{chat_id}"),
            InlineKeyboardButton(f"Language: {settings['language']}", callback_data=f"lang_info:{chat_id}"),
            InlineKeyboardButton("➡️", callback_data=f"lang_inc:{chat_id}"),
        ],
        [
            InlineKeyboardButton("Soft warn", callback_data=f"soft_warn_info:{chat_id}"),
            InlineKeyboardButton(f"{TEXTS[settings["soft_warn"]]}", callback_data=f"soft_warn_toogle:{chat_id}"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

@user_admin
async def get_settings_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is None or update.effective_message is None or update.effective_user is None:
        return
    
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user

    if context.args is None or len(context.args) != 2 and update.effective_chat.type == "private":
        await message.reply_text(get_dialog("CANT_USE_COMMAND_IN_DMS", chat_id=chat.id))
        return

    try:
        chat_id = (await context.bot.get_chat(chat_id=int(context.args[0]))).id
    except:
        if update.effective_chat.type == "private":
            await message.reply_text(get_dialog("CANT_USE_COMMAND_IN_DMS", chat_id=chat.id))
            return

    chat_id = chat.id
    settings = get_settings(chat_id=chat.id)

    if settings["change_settings_creator_only"] is True and (await chat.get_member(user_id=user.id)).status != "creator":
        await message.reply_text(get_dialog("CREATOR_ONLY", chat_id=chat.id))
        return

    reply_markup = build_keyboard(chat_id=chat.id, settings=settings)
    try:
        await context.bot.send_message(chat_id=user.id, text=get_dialog("SETTINGS_PANEL", chat_id).format(id=chat_id), reply_markup=reply_markup)
    except error.Forbidden:
        bot_username = (await context.bot.get_me()).username
        if bot_username is None:
            LOGGER.error("bot_username is null")
            return
        await message.reply_text(text=get_dialog("START_DM_WITH_BOT", chat_id=chat_id))
        return
    
    await message.reply_text(text=get_dialog("SENT_IN_DM", chat_id=chat.id))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is None or update.effective_message is None or update.effective_user is None:
        LOGGER.error("SMTH is null", exc_info=True)
        return 

    # get callback_data
    data = query.data
    if data is None:
        LOGGER.error("data is null")
        return
    
    data_splitted = data.split(":")
    if len(data_splitted) != 2:
        LOGGER.error(f"len(data_splitted) != 2\ndata_splitted: {data_splitted}")
        return
    
    action = data_splitted[0]
    chat_id = int(data_splitted[1])
    text = update.effective_message.text or get_dialog("SETTINGS_PANEL", lang="pl").format(id=chat_id)

    settings = get_settings(chat_id=chat_id)

    # validate user
    chat_member = await context.bot.get_chat_member(chat_id=chat_id, user_id=update.effective_user.id)
    if not (chat_member.status == "creator" or chat_member.status == "administrator" and settings["change_settings_creator_only"] is False):
        await query.answer(get_dialog("NO_PERMISSIONS_TO_CHANGE_SETTINGS", chat_id=chat_id), show_alert=True)
        return

    setting = None
    value = None
    match(action):
        case "lang_dec":
            setting = "language"
            value = get_prev_key(LANG, settings[setting])
            text = get_dialog("SETTINGS_PANEL", lang=value).format(id=chat_id)
        case "lang_inc":
            setting = "language"
            value = get_next_key(LANG, settings[setting])
            text = get_dialog("SETTINGS_PANEL", lang=value).format(id=chat_id)
        case "soft_warn_toogle":
            setting = "soft_warn"
            value = not settings[setting]
        case "soft_warn_info":
            await query.answer(get_dialog("SOFT_WARN_INFO", chat_id=chat_id), show_alert=True)
            return

    await query.answer()
    
    if setting is None or value is None:
        LOGGER.error(f"setting or value is null: {setting}, {value}")
        return
    
    set_setting(chat_id=chat_id, setting=setting, value=value)
    settings = get_settings(chat_id=chat_id)

    reply_markup = build_keyboard(chat_id=chat_id, settings=settings)

    await query.edit_message_text(text=text, reply_markup=reply_markup)

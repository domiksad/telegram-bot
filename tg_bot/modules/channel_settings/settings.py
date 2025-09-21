import json
from datetime import timedelta, datetime, timezone

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, CallbackQuery, error
import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from tg_bot.modules.sql.groups_tracker import get_groups
from tg_bot.modules.sql.settings import * 
from tg_bot.modules.helper_funcs.chat_status import bot_admin, user_admin
from tg_bot.modules.helper_funcs.array_funcs import get_next_key, get_prev_key
from tg_bot.modules.language import get_dialog, LANG
from tg_bot.modules.misc_actions.welcome import TYPES_OF_MSG
from tg_bot import LOGGER


TEXTS = ["❌ Off", "✅ On"] # False (0); True (1)

def build_keyboard(chat_id: int, settings: dict, keyboard_id: str = "main") -> InlineKeyboardMarkup:
    LOGGER.info(f"BUILING KEYBOARD. Settings: {settings.items()}")
    wm = json.loads(settings["welcome_message"])

    CATEGORY_NAMES = ["main", "misc", "welcome"]
    def prepare_data(id: int, func: str):
        return f"{CATEGORY_NAMES[id]}:{func}:{chat_id}"

    keyboard = { # callback can have max 64 chars
        CATEGORY_NAMES[0]: [
            [
                InlineKeyboardButton("Settings", callback_data=prepare_data(0, "dummy")),
            ],
            [
                InlineKeyboardButton("Welcome message settings", callback_data=prepare_data(2, "move")),
            ],
            [
                InlineKeyboardButton("Miscellaneous", callback_data=prepare_data(1, "move")),
            ],
        ],
        CATEGORY_NAMES[1]: [
            [
                InlineKeyboardButton("⬅️", callback_data=prepare_data(1, "lang_dec")),
                InlineKeyboardButton(f"Language: {settings['language']}", callback_data=prepare_data(1, "lang_info")),
                InlineKeyboardButton("➡️", callback_data=prepare_data(1, "lang_inc")),
            ],
            [
                InlineKeyboardButton("Soft warn", callback_data=prepare_data(1, "soft_warn_info")),
                InlineKeyboardButton(f"{TEXTS[settings["soft_warn"]]}", callback_data=prepare_data(1, "soft_warn_toogle")),
            ],
            [
                InlineKeyboardButton(f"Back", callback_data=prepare_data(0, "move")),
            ]
        ],
        CATEGORY_NAMES[2]: [
            [
                InlineKeyboardButton("Welcome message", callback_data=prepare_data(2, "dummy")),
            ],
            [
                InlineKeyboardButton("⬅️", callback_data=prepare_data(2, "welcome_type_dec")),
                InlineKeyboardButton(f"Type: {wm["type"]}", callback_data=prepare_data(2, "welcome_info")),
                InlineKeyboardButton("➡️", callback_data=prepare_data(2, "welcome_type_inc")),
            ],
            [
                InlineKeyboardButton("Check content", callback_data=prepare_data(2, "welcome_content_check")),
                InlineKeyboardButton("Set content", callback_data=prepare_data(2, "welcome_content_set")),
            ] if wm["type"] != "none" else None, # if type == none than we dont have data to show 
            [
                InlineKeyboardButton(f"Back", callback_data=prepare_data(0, "move")),
            ]
        ]
    }

    keyboard = [row for row in keyboard[keyboard_id] if row is not None] # Delete all None rows 

    return InlineKeyboardMarkup(keyboard)

@user_admin
async def get_settings_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is None or update.effective_message is None or update.effective_user is None:
        return
    
    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user

    # DM chat
    if update.effective_chat.type == "private": 
        # Get all groups containing the user
        groups = get_groups()
        groups_with_user = []
        for group_id in groups:
            try:
                group_member = await context.bot.get_chat_member(chat_id=group_id, user_id=user.id) # Rate limiter will kick in for sure
                if group_member.status in ["creator","administrator"]:
                    groups_with_user.append(group_id)
            except error.Forbidden:
                LOGGER.error(f"Forbidden: {group_id}")
        
        keyboard = []
        for group_id in groups_with_user:
            group = await context.bot.get_chat(group_id)
            keyboard.append([
                InlineKeyboardButton(group.title or str(group.id), callback_data=f"main:move:{group_id}")
            ])
            await update.effective_chat.send_message(text=get_dialog("SELECT_GROUP", lang="eng"), reply_markup=InlineKeyboardMarkup(keyboard))
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
    if query is None or update.effective_message is None or update.effective_user is None or update.effective_chat is None or context.user_data is None:
        LOGGER.error("SMTH is null", exc_info=True)
        return 

    # get callback_data
    data = query.data
    if data is None:
        LOGGER.error("data is null")
        return
    
    data_splitted = data.split(":")
    if len(data_splitted) != 3:
        LOGGER.error(f"len(data_splitted) != 3\ndata_splitted: {data_splitted}")
        return
    
    keyboard_id = data_splitted[0]
    action = data_splitted[1]
    chat_id = int(data_splitted[2])
    text = update.effective_message.text or get_dialog("SETTINGS_PANEL", lang="pl").format(id=chat_id)

    settings = get_settings(chat_id=chat_id)

    # validate user
    chat_member = await context.bot.get_chat_member(chat_id=chat_id, user_id=update.effective_user.id)
    if not (chat_member.status == "creator" or chat_member.status == "administrator" and settings["change_settings_creator_only"] is False):
        await query.answer(get_dialog("NO_PERMISSIONS_TO_CHANGE_SETTINGS", chat_id=chat_id), show_alert=True)
        return

    setting = None
    value = None
    match(action.split("_", 1)):
        case ["lang", sub]:
            setting = "language"
            if sub == "dec":
                value = get_prev_key(LANG, settings[setting])
            elif sub == "inc":
                value = get_next_key(LANG, settings[setting])
            elif sub == "info":
                await query.answer()
                return
            else:
                LOGGER.info("ERROR")
                return
            text = get_dialog("SETTINGS_PANEL", lang=value).format(id=chat_id)

        case ["soft", sub]:
            if sub == "warn_toogle":
                setting = "soft_warn"
                value = not settings[setting]
            if sub == "warn_info":
                await query.answer(get_dialog("SOFT_WARN_INFO", chat_id=chat_id), show_alert=True)
                return

        case ["welcome", sub]:
            setting = "welcome_message"
            json_data = json.loads(settings["welcome_message"])
            
            if sub == "type_dec":
                json_data["type"] = get_prev_key(TYPES_OF_MSG, json_data["type"])
            elif sub == "type_inc":
                json_data["type"] = get_next_key(TYPES_OF_MSG, json_data["type"])
            elif sub == "content_check":
                handler = TYPES_OF_MSG[json_data["type"]]
                if handler:
                    await update.effective_chat.send_message(get_dialog("CURRENT_MEDIA", chat_id=chat_id))
                    await handler(update, context, json_data["content"] or "NULL")
                    return
                else:
                    LOGGER.error(f"No handler specified: {json.dumps(json_data)}")
                    return
            elif sub == "content_set":
                if json_data["type"] == "none": # rebuild keyboard because wrong data is set
                    reply_markup = build_keyboard(chat_id=chat_id, settings=settings)
                    await query.edit_message_text(text=text, reply_markup=reply_markup)
                    return
                
                await update.effective_chat.send_message(get_dialog("SEND_NEW_WELCOME_MESSAGE", chat_id=chat_id))
                context.user_data["awaiting_welcome_content"] = {"chat_id": chat_id, "type": json_data["type"], "expires_at": datetime.now(timezone.utc) + timedelta(minutes=5)}
                return
            else:
                LOGGER.info("ERROR")
                return
            value = json.dumps(json_data)
        
        case ["dummy"]:
            await query.answer()
            return

        case ["move"]:
            text = get_dialog("SETTINGS_PANEL", lang=settings["language"]).format(id=chat_id)

    await query.answer()
    
    if setting and value:
        set_setting(chat_id=chat_id, setting=setting, value=value)
    
    settings = get_settings(chat_id=chat_id)

    reply_markup = build_keyboard(chat_id=chat_id, settings=settings, keyboard_id=keyboard_id)

    await query.edit_message_text(text=text, reply_markup=reply_markup)

# Fix json injection
async def dm_handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message is None or update.effective_user is None or update.effective_chat is None or context.user_data is None:
        return

    if "awaiting_welcome_content" in context.user_data:
        data = context.user_data.pop("awaiting_welcome_content")
        if data is None:
            LOGGER.error("No data")
            return
        
        chat_id = data["chat_id"]
        msg_type = data["type"]

        if datetime.now(timezone.utc) > data["expires_at"]:
            await update.effective_message.reply_text(get_dialog("INPUT_EXPIRED", chat_id=chat_id))
            return

        json_data = get_settings(chat_id=chat_id)["welcome_message"]
        json_data = json.loads(json_data)
        
        if update.effective_message.text and msg_type == "text":
            new_content = update.effective_message.text
        elif update.effective_message.photo and msg_type == "img":
            new_content = update.effective_message.photo[-1].file_id
        elif update.effective_message.animation and msg_type == "gif":
            new_content = update.effective_message.animation.file_id
        elif update.effective_message.sticker and msg_type == "sticker":
            new_content = update.effective_message.sticker.file_id
        else:
            await update.effective_message.reply_text(get_dialog("UNSUPPORTED_MESSAGE_TYPE", chat_id=chat_id))
            return

        json_data["type"] = msg_type
        json_data["content"] = new_content

        set_setting(chat_id=chat_id, setting="welcome_message", value=json.dumps(json_data))

        handler = TYPES_OF_MSG[msg_type]
        if handler:
            await update.effective_message.reply_text(get_dialog("WELCOME_MESSAGE_SET", chat_id=chat_id))
            await handler(update, context, json_data["content"])
        else:
            LOGGER.error(f"No handler specified: {json.dumps(json_data)}")
            return
        return
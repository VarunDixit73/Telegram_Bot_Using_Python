from telegram.callbackquery import CallbackQuery
from telegram.ext import callbackcontext, updater
from telegram import Update
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext.updater import Updater
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.ext import CommandHandler
from translate import Translator


def select_lang(update: Update, context: callbackcontext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Hindi",callback_data="Hindi"),
            InlineKeyboardButton("Spanish",callback_data="Spanish"),
            InlineKeyboardButton("German",callback_data="German")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Say Hello!', reply_markup=reply_markup)


lang = ""


def button(update: Update, context: callbackcontext.CallbackContext) -> None:
    global lang
    lang = update.callback_query.data.lower()
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"{query.data} has been selected for translation! You can start translating your text.")
    

def lang_translator(user_input):
    translator = Translator(from_lang="english", to_lang = lang)
    translation = translator.translate(user_input)
    return translation

def reply(update, context):
    user_input = update.message.text
    update.message.reply_text(lang_translator(user_input))

def main():
    api = open("config.env","r")
    updater = Updater(api.read(), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', select_lang))
    dp.add_handler(CommandHandler('select_lang',select_lang))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text, reply))
    updater.start_polling()
    updater.idle()

main()

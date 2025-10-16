# автоматическое форматирование кода Alt+Shift+F
# перезапуск бота  стрелка вверх + Enter

import logging
import os

from dotenv import load_dotenv
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram._utils.types import ReplyMarkup
from telegram.constants import ReplyLimit
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    PicklePersistence,
)

from handlers.progrev_handlers import start, get_answer, get_name, get_number, get_mail, get_agree
from config.states import FIRST_MASSAGE, GET_NAME, GET_NUMBER, GET_MAIL, GET_AGREE, GET_INFO, GET_INLINE_BUTTON, GET_CHOICE
from config.config import TELEGRAM_TOKEN
from handlers.lead_magnet_handlers import get_info, get_inline_button, get_choice
from db.database import create_tables

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger('httpx').setLevel(logging.WARNING)


if __name__ == "__main__":
    persistens = PicklePersistence(filepath='i_fit_bot')
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).persistence(persistens).post_init(create_tables).build()

    # handler - это обработчик который будет обрабатывать команды(что угодно)
    # CommandHandler - это обработчик , который будет обрабатывать команды
    # MessageHandler - это обработчик, который будет обрабатывать сообщения
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FIRST_MASSAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, callback=get_answer)
            ],
            GET_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, callback=get_name)
            ],
            GET_NUMBER: [MessageHandler(filters.CONTACT, callback=get_number)],
            GET_MAIL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, callback=get_mail)
            ],
            GET_AGREE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, callback=get_agree),
                CallbackQueryHandler(callback=get_inline_button)
            ],
            GET_INFO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, callback=get_info),
                
            ],
            GET_INLINE_BUTTON: [
                CallbackQueryHandler(callback=get_inline_button)
            ],
            GET_CHOICE: [
                CallbackQueryHandler(callback=get_choice)
            ]
        },
        fallbacks=[CommandHandler("start", start)],
        persistent=True,
        name="conv_handler"
    )

    application.add_handler(conv_handler)

    application.run_polling()

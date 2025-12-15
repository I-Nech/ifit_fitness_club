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
from config.states import FIRST_MASSAGE, GET_NAME, GET_NUMBER, GET_MAIL, GET_AGREE, GET_INFO, GET_INLINE_BUTTON, GET_CHOICE, ADMIN_START
from config.config import TELEGRAM_TOKEN
from handlers.lead_magnet_handlers import get_info, get_inline_button, get_choice, get_more_info, get_inline_video 
from db.database import create_tables
from logs.logger import logger
from handlers.admins_handler import admins_start, users_list, csv_users_list, spam_send_messages, new_users_list
# tags_list, new_tags_list, not_new_tags_list, csv,
load_dotenv()


async def abc(update, context):
    print(update.effective_message.video.file_id)

if __name__ == "__main__":
    persistence = PicklePersistence(filepath='i_fit_bot')
    persistence_path = 'i_fit_bot'
    if os.path.exists(persistence_path):
        if os.stat(persistence_path).st_size == 0:
            print(f"Файл {persistence_path} пустой. Удаляю для сброса состояния.")
            os.remove(persistence_path)
        else:
            print(f"Файл {persistence_path} существует и не пустой.")
    else:
        print(f"Файл {persistence_path} не найден, он будет создан при запуске.")


    persistence = PicklePersistence(filepath=persistence_path)
    persistence = PicklePersistence(filepath='i_fit_bot')
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).persistence(persistence).post_init(create_tables).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FIRST_MASSAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, callback=get_answer),
                MessageHandler(filters.VIDEO, callback=abc)
            ],
            GET_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, callback=get_name)
            ],
            GET_NUMBER: [MessageHandler(filters.CONTACT, callback=get_number)],
            GET_MAIL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, callback=get_mail)
            ],
            GET_AGREE: [
                MessageHandler(filters.Regex('^(Да|Нет)$'), callback=get_agree), # РЕГУЛЯРКА
                CallbackQueryHandler(callback=get_inline_button)
            ],
            GET_INFO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, callback=get_info),   
            ],
            GET_INLINE_BUTTON: [
                CallbackQueryHandler(pattern="Узнать больше",callback=get_more_info),
                CallbackQueryHandler(pattern="^(Пилатес|НЯП)$",callback=get_inline_video),
                CallbackQueryHandler(pattern="^Вернуться к списку$",callback=get_info),
                CallbackQueryHandler(callback=get_inline_button)
            ],
            GET_CHOICE: [
                CallbackQueryHandler(pattern="Узнать больше",callback=get_more_info),
                CallbackQueryHandler(callback=get_choice)
            ],

            #ADMIN HANDLERS
            ADMIN_START: [
                CallbackQueryHandler(callback=users_list, pattern='users_list'),
                # CallbackQueryHandler(callback=tags_list, pattern='tags_list'),
                CallbackQueryHandler(callback=new_users_list, pattern='new_users_list'),
                # CallbackQueryHandler(callback=not_new_tags_list, pattern='notnew_tags_list'),
                CallbackQueryHandler(callback=csv_users_list, pattern='csv_users_list'),
                CallbackQueryHandler(callback=spam_send_messages, pattern='spam_send_message'),
            ]
        },
        fallbacks=[CommandHandler("start", start)],
        persistent=True,
        name="conv_handler"
    )

    application.add_handler(conv_handler)
    logger.info("БОТ ЗАПУЩЕН 🟩")
    application.run_polling()
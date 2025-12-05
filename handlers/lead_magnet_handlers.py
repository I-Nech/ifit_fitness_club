from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ContextTypes,
)
from config.states import GET_INLINE_BUTTON, GET_CHOICE
from config.texts import lead_magnets
from logs.logger import logger 

async def get_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Петли TRX", callback_data="Петли")],
        [InlineKeyboardButton("Пилатес", callback_data="Пилатес")],
        [InlineKeyboardButton("Soft fitness", callback_data="Soft fitness")],
        [InlineKeyboardButton("90-60-90", callback_data="90-60-90")],
        [InlineKeyboardButton("Степ + сила", callback_data="Степ + сила")],
        [InlineKeyboardButton("Ноги, ягодицы, пресс", callback_data="НЯП")],
        [InlineKeyboardButton("45/15", callback_data="45/15")],
        [InlineKeyboardButton("FITMIX", callback_data="FITMIX")],
        [InlineKeyboardButton("Стретчинг", callback_data="Стретчинг")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="получайте гайд",
        reply_markup=markup,
    )
    return GET_INLINE_BUTTON


async def get_inline_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [
            InlineKeyboardButton(
                "Вернуться к списку", callback_data="Вернуться к списку"
            )
        ],
        [
            InlineKeyboardButton(
                "Узнать больше о клубе IFIT", callback_data="Узнать больше"
            )
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.answer()
    logger.info('ОШИБКА ТУТ 😡')
    lead_magnet = lead_magnets[query.data]
    # /-начиная от корня ./ - текущая папка ../ - на папку назад
    # photo = open("./static/trx.jpg", "rb")
    photo = open(lead_magnet["image"], "rb")
    # что если пилатес то send_video
    caption = lead_magnet["caption"] + "\n" + lead_magnet["text"]
    if len(caption) < 1024:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=caption,
            reply_markup=markup,
        )
    
    else:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=lead_magnet["caption"],
        )
        logger.info('ОШИБКА ТУТ 🥶')
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=lead_magnet["text"],
            reply_markup=markup,
        )
        logger.info('ОШИБКА ТУТ 🤡')
    photo.close()
    return GET_CHOICE

    if query.data == "yes":
        query = update.callback_query
        await query.delete_message()  # можно сделать только инлайн кнопаками
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Спасибо за ответ! Я всегда буду тут, напиши /start если захочешь снова получить гайд.",
        )

        # context.user_data.clear() #- удаление словаря с данными пользователя
        # await query.answer('Спасибо за ответ!', show_alert=True)
        # await query.answer('Спасибо за ответ!')
        # await query.answer() # ответ может быть пустой


async def get_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "Вернуться к списку":
        return await get_info(update, context)


async def get_more_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [
            InlineKeyboardButton(
                "Наш инcтаграм", url="https://www.instagram.com/ifit_fitnessclub"
            ),
            InlineKeyboardButton(
                "Вернуться к списку", callback_data="Вернуться к списку"
            )
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.answer()
    lead_magnet = lead_magnets[query.data]
    # /-начиная от корня ./ - текущая папка ../ - на папку назад
    # photo = open("./static/trx.jpg", "rb")
    photo = open(lead_magnet["image"], "rb")
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo,
        caption=lead_magnet["caption"] + "\n" + lead_magnet["text"],
        reply_markup=markup,
    )
    photo.close()
    return GET_INLINE_BUTTON

async def get_inline_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [
            InlineKeyboardButton(
                "Вернуться к списку", callback_data="Вернуться к списку"
            )
        ],
        [
            InlineKeyboardButton(
                "Узнать больше о клубе IFIT", callback_data="Узнать больше"
            )
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.answer()
    lead_magnet = lead_magnets[query.data]
    
   
    if len(lead_magnet["text"]) < 1024:
        #video= open(lead_magnet["video"], "rb")
        await context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=lead_magnet['file_id'],
            caption=lead_magnet["caption"] + "\n" + lead_magnet["text"],
            reply_markup=markup,
        )
    else:
        #video= open(lead_magnet["video"], "rb")
        await context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=lead_magnet['file_id'],
            caption=lead_magnet["caption"],
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=lead_magnet["text"],
            reply_markup=markup,
        )

    
    return GET_CHOICE
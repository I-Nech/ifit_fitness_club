import csv
import asyncio
from telegram import (Update, InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import ContextTypes
from config.config import ADMIN_ID
from config.states import ADMIN_START
from db.users_crud import get_users
from db.user_tags_crud import (get_users_by_tag,)
from logs.logger import logger


async def admins_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keybord = [
        [InlineKeyboardButton('Список пользователей', callback_data = 'users_list')],
        [InlineKeyboardButton('Список тегов', callback_data='tags_list')],
        [InlineKeyboardButton('Список пользователей с тегом НОВЫЙ', callback_data='new_users_list')],
        [InlineKeyboardButton('Список пользователей с тегом НЕ НОВЫЙ', callback_data='notnew_tags_list')],
        [InlineKeyboardButton('Список пользователей с тегом CSV', callback_data='csv_users_list')],
        [InlineKeyboardButton('Рассылка', callback_data='send_message')],
    ]
    murkup = InlineKeyboardMarkup(keybord)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет админ!", reply_markup=murkup)
    return ADMIN_START


async def users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await get_users()
    text = 'Список пользователей:\n'
    text += '№ - Ссылка - Телефон - Email\n'
    for n, user in enumerate(users, 1):
        logger.info(f'Пользователь{user} есть✅')
        text += f'{n}.- {user[2]} - (tg://user?id={user[1]}) - {user[3]} - {user[4]}\n'
        logger.info(f'{text} создан ✳️')
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text,
        # parse_mode='MarkdownV2',
    )
    logger.info('НЕ ДАЕТ СДЕЛАТЬ ЧЕРЕЗ МАРКДАУН ⛔️')
    await admins_start(update, context)

async def csv_users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await get_users()
    with open('users.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['№', 'Ссылка', 'Телефон', 'Email'])
        for n, user in enumerate(users, 1):
            writer.writerow([n, user[2], user[3], user[4]])

    await context.bot.send_document(
        chat_id=update.effective_user.id,
        document=open('users.csv', 'rb'),
        caption='Список пользователей CSV'
    )
    return admins_start(update, context)

async def spam_send_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await get_users()
    for user in users():
        try:
            await context.bot.send_message(
                chat_id=user[1],
                text=f'Привет! У нас появилась новая тренировка!'
            )
            await asyncio.sleep(0.07)
        except Exception as e:
            logger.error(f'Ошибка при отправке сообщения пользователю {user[1]}: {e}')
            continue
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text='Рассылка завершена',
    )
    logger.info(f'Рассылка завершена')
    await admins_start(update, context)

# async def new_tags_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     tag_id = await get_user_tag_id()
#     user_id_tg = await get_user_tag_id()
#     text = 'Список новых пользователей :\n'
#     text += 'khbjhbjhvbjhnvb\n'
#     for tag_id in user_tags():
#         if tag_id == 1:
#             text += user_id_tg

async def new_users_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = 'Список пользователей c тэгом "новый" :\n'
    user_tags_data = await get_users_by_tag("новый")
    for user_data in user_tags_data:
        text += f'{user_data['id_tg']}\n'
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=text,
    )
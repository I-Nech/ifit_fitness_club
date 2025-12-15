
from datetime import timedelta
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    
)
from telegram.ext import (
    ContextTypes,
)
from config.states import (
    FIRST_MASSAGE,
    GET_NAME,
    GET_NUMBER,
    GET_MAIL,
    GET_AGREE,
    GET_INFO,
    GET_INLINE_BUTTON,
)
from config.config import ADMIN_ID
# import os

from utils.escape_symvol import escape_symvol
import asyncio
from handlers.jobs import send_job_message
from datetime import timedelta
from config.texts import text_1
from db.users_crud import create_user,get_user , update_user
from logs.logger import logger
from db.user_tags_crud import create_user_tag, rename_user_tag
from config.config import ADMIN_ID
from handlers.admins_handler import admins_start
from config.jobtexsts import jobtext

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if update.effective_user.id == int(ADMIN_ID):
        return await admins_start(update, context)

    if not await get_user(update.effective_user.id):
        await  create_user(update.effective_user.id)
        logger.info(f'Пользователь{update._effective_user.id} создан 👍')
        await create_user_tag(update.effective_user.id, 'новый') 
        logger.info(f'ТЭГ НОВЫЙ {update._effective_user.id} добавлен в таблицу user_tags ✌️')

    elif await get_user(update._effective_user.id):
       logger.info(f'Пользователь{update._effective_user.id} снова пришел ❤️') 
       await rename_user_tag(update.effective_user.id,'новый', 'не новый')
       logger.info(f'Пользователь{update._effective_user.id} добавлен в таблицу user_tags 🆗') 
       
    keyboard = [["Да", "Нет"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=escape_symvol(text_1),
        reply_markup=markup,
        parse_mode="MarkdownV2",
    )
    job = context.job_queue.run_once(
        send_job_message,
        when=timedelta(seconds=30),
        data={"message": jobtext["Первый"]},
        name=f"send_job_message_{update.effective_user.id}", 
        chat_id=update.effective_user.id,
    )
    context.user_data['job_name'] = job.name
    return FIRST_MASSAGE

async def get_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.effective_message.text
    if "job_name" in context.user_data:
        job_name = context.user_data.pop('job_name')
        for jobs in context.job_queue.get_jobs_by_name(job_name):
            jobs.schedule_removal()
       
    if answer == "Да":
        keyboard = [[update.effective_user.first_name]]
        markup = ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True, one_time_keyboard=True
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Чтобы получить консультацию, напиши свое имя.",
            reply_markup=markup,
        )

        job = context.job_queue.run_once(
        send_job_message,
        when=timedelta(seconds=30),
        data={"message": jobtext["Второй"]},
        name=f"send_job_message_{update.effective_user.id}", 
        chat_id=update.effective_user.id,
    )
        context.user_data['job_name'] = job.name      
        return GET_NAME
    elif answer.lower() in ["нет"]:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Очень жаль, может быть в другой  раз...",
            reply_markup=ReplyKeyboardRemove(),
        )
        return GET_NAME
    else:
        keyboard = [["Да", "Нет"]]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Пожалуйста, выберите вариант ответа из представленных ниже',
        reply_markup=markup,
        parse_mode="MarkdownV2",
    )
    job = context.job_queue.run_once(
        send_job_message,
        when=timedelta(seconds=30),
        data={"message": "Это всего лишь маленький опрос 🙃 поговори со мной", 'markup':markup},
        name=f"send_job_message_{update.effective_user.id}", 
        chat_id=update.effective_user.id,
    )
    context.user_data['job_name'] = job.name
    return FIRST_MASSAGE

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_message.text

    if "job_name" in context.user_data:
        job_name = context.user_data.pop('job_name')
        for jobs in context.job_queue.get_jobs_by_name(job_name):
            jobs.schedule_removal()

    await update_user(update.effective_user.id, name=name)
    context.user_data["name"] = name
    
    keyboard = [[KeyboardButton("Поделиться моим контактом", request_contact=True)]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Чтобы продолжить, нажмите на 'поделиться контактом'.",
        reply_markup=markup,
    )
    return GET_NUMBER

async def get_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.effective_message.contact.phone_number
    await update_user(update.effective_user.id, number=number)
    context.user_data["number"] = number
    print(number)
    if number[:4] != "+375" or number[:4] != "3750" or number[:4] != "3750":
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Напишите свой e-mail.", reply_markup=ReplyKeyboardRemove()
        )
        return GET_MAIL

async def get_mail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mail = update.effective_message.text
    await update_user(update.effective_user.id, email=mail)
    context.user_data["mail"] = mail
    print(mail)
    keyboard = [["Да", "Нет"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Вы согласны на обработку персональных данных? Мы не передаем ваши данные третьим лицам.",
        reply_markup=markup,
    )
    return GET_AGREE

async def get_agree(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.effective_message.text
    if answer == "Да":
        keyboard = [["FIT"]]
        markup = ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True, one_time_keyboard=True
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Добро пожаловать в клуб! Жми FIT и получай гайд по тренировкам",
            reply_markup=markup,
        )
        await context.bot.send_message(
            chat_id=ADMIN_ID, text= f'{context.user_data}'
        )
        return GET_INFO
    else:
        keyboard = [[InlineKeyboardButton("Да", callback_data="yes")]]
        markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Тогда все!(",
            reply_markup=markup
        )

    

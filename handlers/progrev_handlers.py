from bdb import effective
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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update -  это полная информация о том что произошло в чате(сообщении)
    # update.effective_user - это информация о пользователе, который отправил сообщение
    # update.effective_chat - это информация о чате в котром произошло событие(информация о диологе:диалг напр с ботом,
    #  группой и т)
    # update.effective_message - это информация о сообщении , которое отправил пользователь
    # context - это контекст, в котором происходит событие(побочные действия котрые наш бот будет уметь делать(в контексте
    # будем данные между разными функциями передавать, будем что-то запоминать, будем вызывать отложенные действия,
    # вспомогательные действия которые он будет делать))
    
    if not await get_user(update.effective_user.id):
        await  create_user(update.effective_user.id)
    
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
        data={"massage": "соберись"},
        name=f"send_job_message_{update.effective_user.id}",
        chat_id=update.effective_user.id,
    )
    context.user_data['job_name'] = job.name
    
    # await context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text="соберись.",
    #     reply_markup=markup,
    # )
    context.user_data['job'] = job
    return FIRST_MASSAGE


async def get_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['job'].schedule_removal()
    answer = update.effective_message.text
    if "job_name" in context.user_data:
        for jobs in context.job_queue.get_jobs_by_name(context.user_data['job_name']):
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
        return GET_NAME
    elif answer == "Нет":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Очень жаль, может быть в другой  раз...",
            reply_markup=ReplyKeyboardRemove(),
        )
        return GET_NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_message.text
    await update_user(update.effective_user.id)
    context.user_data["name"] = name
    
    keyboard = [[KeyboardButton("Поделиться моим контактом", request_contact=True)]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Чтобы продолжить, поделитесь контактом.",
        reply_markup=markup,
    )
    return GET_NUMBER


async def get_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.effective_message.contact.phone_number
    # await update_user(update.effective_user.id, number)
    context.user_data["number"] = number
    print(number)
    if number[:4] != "+375" or number[:4] != "3750" or number[:4] != "3750":
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Напишите свой e-mail."
        )
        return GET_MAIL


async def get_mail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mail = update.effective_message.text
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

    print(context.user_data)

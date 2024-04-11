# Импортируем необходимые классы.
import logging
import os
import sqlite3

import telegram
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackContext, ConversationHandler
from dotenv import load_dotenv
from yandexgptlite import YandexGPTLite


account = YandexGPTLite('b1gd73t8icljbi3n5jnm',
                        'y0_AgAAAAA8mYxyAATuwQAAAAEA4VtUAACenuIdFgtGrKt6F_TFoBQ-tX8r2Q')

load_dotenv()

BOT_TOKEN = os.getenv('TOKEN')

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def on_start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    await update.message.reply_text('Привет я бот, который поможет тебе ответить почти на каждый вопрос!'
                                    ' Для большей информации напиши /help',
                                    reply_markup=ReplyKeyboardMarkup([['/start'], ['/stop'], ['/help']]))
    return 1


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text('''
/q - задать вопрос,
/add_date - добавить дату в календарь(формат(...)),
/show_calendar - показать расписание на какой-то день, 
/stop.''')


async def stop(update, context):
    await update.message.reply_text('До скорого, мой любознательный друг!')
    return ConversationHandler.END


async def q_and_a(update, context):
    text = account.create_completion(update.message.text, '1', system_prompt='отвечай на русском')
    await update.message.reply_text(text)


async def add_date(update, context):
    user = update.effective_user
    print(user.first_name[:1])
    print(user.mention_html)
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!",
    )


async def show_calendar(update, context):
    pass


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", on_start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("q", q_and_a))
    application.add_handler(CommandHandler("add_date", add_date))
    application.add_handler(CommandHandler("show_calendar", show_calendar))
    application.run_polling()


if __name__ == '__main__':
    main()

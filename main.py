# Импортируем необходимые классы.
import logging
import os
from data.dates import Data

import telegram
from data import db_session
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
/q - задать вопрос(формат(/q вопрос)),
/add - добавить дату в календарь(формат(/add дд.мм.гг, событие)),
/show_calendar - показать расписание на какой-то день(формат(/show_calendar дд.мм.гг)), 
/stop.''')


async def stop(update, context):
    await update.message.reply_text('До скорого, мой любознательный друг!')
    return ConversationHandler.END


async def q_and_a(update, context):
    text = account.create_completion(update.message.text, '1', system_prompt='отвечай на русском')
    await update.message.reply_text(text)


async def add_date(update, context):
    dt = Data()
    db_sess = db_session.create_session()
    user = update.effective_user
    message = update.message.text
    stroka = message.split()[1:]
    date = str(stroka[0])
    event = str(' '.join(stroka[1:]))
    print(user.first_name[:1])
    dt.name = str(user.first_name[:1])
    dt.date = date
    dt.event = str(event)
    db_sess.add(dt)
    db_sess.commit()
    await update.message.reply_html(
        rf"Добавил в календарь дату {dt.date} с событием '{dt.event}', от пользователя {dt.name}"
    )


async def show_calendar(update, context):
    dt = Data()
    db_sess = db_session.create_session()
    message = update.message.text
    date = message.split()[1]
    await update.message.reply_html(db_sess.query(Data).filter((Data.name == update.effective_user.first_name[:1]) |
                                                               Data.date == date))


def main():
    db_session.global_init("dates.db")
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

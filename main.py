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
/add_date - добавить дату в календарь(формат(/add дд.мм.гг, событие)),
/del_date - удалить дату из календаря(формат(/del дд.мм.гг, событие)),
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
    dt.date = date.split()[0]
    dt.event = str(event)
    db_sess.add(dt)
    db_sess.commit()
    await update.message.reply_html(
        rf"Добавил в календарь дату {dt.date} с событием '{dt.event}', от пользователя {dt.name}"
    )


async def del_date(update, context):
    dt = Data()
    db_sess = db_session.create_session()
    user = update.effective_user
    message = update.message.text
    stroka = message.split()[1:]
    date = str(stroka[0])
    event = str(' '.join(stroka[1:]))
    print(user.first_name[:1])
    row = (db_sess.query(Data).filter(Data.name == user.first_name[:1])
           .filter(Data.date == date).filter(Data.event == event)).first()
    db_sess.delete(row)
    db_sess.commit()
    await update.message.reply_text(
        rf"Удалил из календаря дату {date} с событием '{event}', от пользователя {user.first_name[0]}"
    )


async def show_calendar(update, context):
    db_sess = db_session.create_session()
    message = update.message.text
    user = str(update.effective_user.first_name[:1]).split()
    date = str(message.split()[1]).split()
    event = db_sess.query(Data.event).filter(Data.name == user[0]).filter(Data.date == date[0]).all()
    print(date[0], user[0])
    vivod = []
    for ev in event:
        print(ev[0])
        vivod.append(ev[0])
    if event:
        await update.message.reply_html(f"В этот день у вас {', '.join(vivod)}")
    else:
        await update.message.reply_html('На этот день нет никаких событий.')


def main():
    db_session.global_init("dates.db")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", on_start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("q", q_and_a))
    application.add_handler(CommandHandler("add_date", add_date))
    application.add_handler(CommandHandler("del_date", del_date))
    application.add_handler(CommandHandler("show_calendar", show_calendar))
    application.run_polling()


if __name__ == '__main__':
    main()

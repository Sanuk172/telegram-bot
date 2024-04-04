# Импортируем необходимые классы.
import logging
import os

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
                                    ' Спроси у меня что-нибудь.',
                                    reply_markup=ReplyKeyboardMarkup([['/enter']]))


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


async def stop(update, context):
    await update.message.reply_text('До скорого, мой любознательный друг!')
    return ConversationHandler.END


async def q_and_a(update, context):
    text = account.create_completion(update.message.text, '0.6', system_prompt='отвечай на русском')
    update.message.reply_text(text)


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', on_start)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, q_and_a)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()

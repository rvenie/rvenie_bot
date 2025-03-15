from datetime import datetime, timedelta
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from config import TELEGRAM_TOKEN
from utils.logging_setup import setup_logger
from utils.network import check_internet
from handlers.command_handlers import (
    start_command, help_command, #model_command, 
    params_command, reset_command, clear_command
)
from handlers.message_handlers import handle_message
from handlers.callback_handlers import button_callback
from handlers.error_handlers import error_handler

# Настройка логирования
logger = setup_logger()

async def clear_cache(context):
    """Очистка данных неактивных пользователей"""
    logger.info("Очистка кэша пользовательских данных...")
    now = datetime.now()
    for user_id in list(context.application.user_data.keys()):
        user_data = context.application.user_data[user_id]
        last_interaction = user_data.get('last_interaction', now)
        if now - last_interaction > timedelta(days=30):
            del context.application.user_data[user_id]
            logger.info(f"Данные пользователя {user_id} удалены.")

def main():
    """Основная функция запуска бота"""
    try:
        # Проверка интернета
        if not check_internet():
            logger.error("Нет подключения к интернету")
            return

        # Создание приложения
        app = (
            Application.builder()
            .token(TELEGRAM_TOKEN)
            .get_updates_pool_timeout(30)
            .get_updates_read_timeout(30)
            .get_updates_write_timeout(30)
            .build()
        )

        # Добавляем обработчики команд
        app.add_handler(CommandHandler('start', start_command))
        app.add_handler(CommandHandler('help', help_command))
        # app.add_handler(CommandHandler('model', model_command))
        app.add_handler(CommandHandler('params', params_command))
        app.add_handler(CommandHandler('reset', reset_command))
        app.add_handler(CommandHandler('clear', clear_command))

        # Добавляем обработчик callback-запросов для кнопок
        app.add_handler(CallbackQueryHandler(button_callback))

        # Добавляем обработчики для разных типов сообщений
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.add_handler(MessageHandler(filters.PHOTO, handle_message))
        app.add_handler(MessageHandler(filters.VOICE, handle_message))
        app.add_handler(MessageHandler(filters.Document.ALL, handle_message))

        # Добавляем глобальный обработчик ошибок
        app.add_error_handler(error_handler)
        
        # Запуск периодической очистки кэша раз в 30 дней
        app.job_queue.run_repeating(clear_cache, interval=30 * 24 * 60 * 60, first=0)

        logger.info('🚀 Бот запущен!')
        app.run_polling(poll_interval=1)

    except Exception as e:
        logger.error(f'❌ Ошибка при запуске бота: {str(e)}')

if __name__ == '__main__':
    main()

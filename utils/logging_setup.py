import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    """Настройка логирования с ротацией файлов"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Ротация файлов логов
    handler = RotatingFileHandler(
        'bot.log', maxBytes=5*1024*1024, backupCount=2, encoding='utf-8'
    )
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Вывод в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Проверка наличия переменных окружения
if not TELEGRAM_TOKEN:
    print("TELEGRAM_TOKEN не установлен в переменных окружения.")
    exit(1)

if not MISTRAL_API_KEY:
    print("MISTRAL_API_KEY не установлен в переменных окружения.")
    exit(1)

# Доступные модели
AVAILABLE_MODELS = {
    "mistral-small-latest": "Бесплатная модель"
    # "mistral-small": "Сбалансированная модель",
    # "mistral-large-latest": "Продвинутая модель"
}

# Параметры по умолчанию
DEFAULT_PARAMS = {
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 0.95
}

# Ограничения
MAX_TEXT_LENGTH = 4000
MAX_PHOTO_SIZE = 5 * 1024 * 1024  # 5 MB
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB
MAX_VOICE_DURATION = 60  # секунды
MAX_DIALOG_HISTORY = 10

from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import DEFAULT_PARAMS, AVAILABLE_MODELS, MAX_DIALOG_HISTORY
from config import MAX_TEXT_LENGTH, MAX_PHOTO_SIZE, MAX_FILE_SIZE, MAX_VOICE_DURATION

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /start"""
    # Инициализация настроек пользователя
    context.user_data['current_model'] = "mistral-small-latest"
    context.user_data['params'] = DEFAULT_PARAMS.copy()
    context.user_data['last_interaction'] = datetime.now()
    context.user_data['dialog_history'] = []

    welcome_message = (
        "👋 Привет! Я бот на базе Mistral AI.\n\n"
        "Доступные команды:\n"
        "/start - начать диалог\n"
        "/help - получить помощь\n"
        # "/model - выбрать модель\n"
        "/params - настроить параметры\n"
        "/reset - сбросить настройки\n"
        "/clear - очистить историю диалога"
    )
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатываем команду /help. Показываем текущие настройки и доступные команды.
    """
    current_model = context.user_data.get('current_model', 'mistral-small-latest')
    params = context.user_data.get('params', DEFAULT_PARAMS)
    history_count = len(context.user_data.get('dialog_history', []))

    help_message = (
        f"🤖 Текущие настройки:\n\n"
        f"Модель: {current_model}\n"
        f"Температура: {params['temperature']}\n"
        f"Макс. токенов: {params['max_tokens']}\n"
        f"Top P: {params['top_p']}\n"
        f"Сохранено сообщений в истории: {history_count}/{MAX_DIALOG_HISTORY}\n\n"
        "Команды:\n"
        # "/model - сменить модель\n"
        "/params - настроить параметры\n"
        "/reset - сбросить настройки\n"
        "/clear - очистить историю диалога\n\n"
        "Ограничения:\n"
        f"Макс. длина текста: {MAX_TEXT_LENGTH} символов\n"
        f"Макс. размер фото: {MAX_PHOTO_SIZE/1024/1024} MB\n"
        f"Макс. размер файла: {MAX_FILE_SIZE/1024/1024} MB\n"
        f"Макс. длительность голосового: {MAX_VOICE_DURATION} сек"
    )
    await update.message.reply_text(help_message)

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатываем команду /clear. Очищаем историю диалога пользователя.
    """
    context.user_data['dialog_history'] = []
    await update.message.reply_text("✅ История диалога очищена")

# Добавляем функции обработки модели, параметров и сброса настроек
# async def model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """
#     Обрабатываем команду /model. Показываем клавиатуру для выбора модели.
#     """
#     keyboard = [
#         [InlineKeyboardButton(f"{model} - {description}", callback_data=f"model_{model}")]
#         for model, description in AVAILABLE_MODELS.items()
#     ]

#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text("Выберите модель:", reply_markup=reply_markup)

async def params_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатываем команду /params. Показываем клавиатуру для настройки параметров.
    """
    keyboard = [
        [InlineKeyboardButton("Температура (0-1)", callback_data="param_temperature")],
        [InlineKeyboardButton("Макс. токенов", callback_data="param_max_tokens")],
        [InlineKeyboardButton("Top P (0-1)", callback_data="param_top_p")],
        [InlineKeyboardButton("Сбросить параметры", callback_data="reset_params")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите параметр для настройки:", reply_markup=reply_markup)

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатываем команду /reset. Сбрасываем настройки пользователя к значениям по умолчанию.
    """
    context.user_data['current_model'] = "mistral-small-latest"
    context.user_data['params'] = DEFAULT_PARAMS.copy()
    await update.message.reply_text("✅ Настройки сброшены к значениям по умолчанию")
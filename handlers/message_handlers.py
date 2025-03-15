from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

from config import MAX_TEXT_LENGTH, MAX_PHOTO_SIZE, MAX_VOICE_DURATION, MAX_FILE_SIZE
from config import DEFAULT_PARAMS, MAX_DIALOG_HISTORY
from utils.network import check_internet
from utils.dialog_history import add_to_dialog_history
from services.mistral_service import get_ai_response

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    """
    Обрабатываем текстовое сообщение от пользователя.
    """
    # Проверяем длину текста
    if len(text) > MAX_TEXT_LENGTH:
        await update.message.reply_text(
            f"❌ Текст слишком длинный. Максимальная длина: {MAX_TEXT_LENGTH} символов."
        )
        return

    # Если пользователь сейчас настраивает параметр
    if 'editing_param' in context.user_data:
        param = context.user_data['editing_param']
        try:
            value = float(text)
            # Проверяем корректность значения параметра
            if param in ['temperature', 'top_p']:
                if not 0 <= value <= 1:
                    await update.message.reply_text("Значение должно быть между 0 и 1")
                    return
            elif param == 'max_tokens':
                if not 1 <= value <= 2000:
                    await update.message.reply_text("Значение должно быть между 1 и 2000")
                    return

            # Обновляем параметр
            context.user_data.setdefault('params', DEFAULT_PARAMS.copy())
            context.user_data['params'][param] = value
            del context.user_data['editing_param']
            await update.message.reply_text(f"Параметр {param} установлен на {value}")
        except ValueError:
            await update.message.reply_text("Пожалуйста, введите корректное числовое значение")
        return

    # Отправляем индикатор печати
    await update.message.chat.send_action(action="typing")
    
    # Добавляем сообщение пользователя в историю
    add_to_dialog_history(context, "user", text)
    
    # Создаем сообщение для ответа, которое будем редактировать
    sent_message = await update.message.reply_text(
        "🤖 Формирую ответ...",
        disable_web_page_preview=True
    )
    
    # Получаем ответ от AI
    response_text = await get_ai_response(context)
    
    # Добавляем ответ AI в историю
    add_to_dialog_history(context, "assistant", response_text)
    
    # Редактируем сообщение с полным ответом вместо отправки нового
    await sent_message.edit_text(
        response_text,
        disable_web_page_preview=True
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатываем входящие сообщения от пользователя.
    """
    # Проверяем наличие подключения к интернету
    if not check_internet():
        await update.message.reply_text("❌ Отсутствует подключение к интернету")
        return
    
    # Обновляем время последнего взаимодействия пользователя
    context.user_data['last_interaction'] = datetime.now()
    
    # Обрабатываем разные типы сообщений
    if update.message.text:
        await handle_text_message(update, context, update.message.text.strip())
    elif update.message.photo:
        await handle_photo(update, context)
    elif update.message.voice:
        await handle_voice(update, context)
    elif update.message.document:
        await handle_document(update, context)
    else:
        await update.message.reply_text(
            "Извините, я могу обрабатывать только текстовые сообщения, фото, "
            "голосовые сообщения и документы."
        )

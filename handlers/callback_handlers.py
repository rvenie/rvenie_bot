from telegram import Update
from telegram.ext import ContextTypes

from config import DEFAULT_PARAMS, AVAILABLE_MODELS

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий кнопок"""
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("model_"):
        # Обработка выбора модели
        model = data.replace("model_", "")
        if model in AVAILABLE_MODELS:
            context.user_data['current_model'] = model
            await query.edit_message_text(f"Выбрана модель: {model}")
        else:
            await query.edit_message_text("❌ Неверная модель.")
            
    elif data.startswith("param_"):
        # Обрабатываем настройку параметров
        param = data.replace("param_", "")
        if param in DEFAULT_PARAMS:
            context.user_data['editing_param'] = param
            current_value = context.user_data.get('params', DEFAULT_PARAMS).get(param, DEFAULT_PARAMS[param])
            await query.edit_message_text(
                f"Введите новое значение для {param} (текущее: {current_value}):"
            )
        else:
            await query.edit_message_text("❌ Неверный параметр.")
    elif data == "reset_params":
        # Сбрасываем параметры к значениям по умолчанию
        context.user_data['params'] = DEFAULT_PARAMS.copy()
        await query.edit_message_text("Параметры сброшены к значениям по умолчанию")
    else:
        await query.edit_message_text("❌ Неизвестное действие.")
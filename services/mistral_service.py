from mistralai import Mistral
from telegram.ext import ContextTypes
import logging

from config import MISTRAL_API_KEY, DEFAULT_PARAMS

# Инициализация клиента Mistral
mistral = Mistral(api_key=MISTRAL_API_KEY)
logger = logging.getLogger(__name__)

async def get_ai_response(context: ContextTypes.DEFAULT_TYPE) -> str:
    """Получение ответа от AI-модели"""
    try:
        current_model = context.user_data.get('current_model', 'mistral-tiny')
        params = context.user_data.get('params', DEFAULT_PARAMS)
        
        # Формирование сообщений для API
        messages = [
            {
                "role": "system",
                "content": "Ты - полезный ассистент, который всегда проверяет факты и дает точные ответы. Отвечай на русском языке."
            }
        ]
        
        # Добавление истории диалога
        dialog_history = context.user_data.get('dialog_history', [])
        for message in dialog_history:
            if message["role"] in ["user", "assistant"]:
                messages.append({
                    "role": message["role"],
                    "content": message["content"]
                })
        
        # Вызов API
        chat_response = mistral.chat.complete(
            model=current_model,
            messages=messages,
            temperature=params['temperature'],
            max_tokens=int(params['max_tokens']),
            top_p=params['top_p']
        )
        
        return chat_response.choices[0].message.content.strip()
        
    except Exception as e:
        logger.error(f"Error in get_ai_response: {str(e)}")
        return "❌ Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже."

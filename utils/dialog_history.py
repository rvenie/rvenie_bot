from datetime import datetime
from telegram.ext import ContextTypes

from config import MAX_DIALOG_HISTORY

def add_to_dialog_history(context: ContextTypes.DEFAULT_TYPE, role: str, content: str, max_history: int = MAX_DIALOG_HISTORY):
    """Добавление сообщения в историю диалога"""
    if 'dialog_history' not in context.user_data:
        context.user_data['dialog_history'] = []
    
    # Добавляем сообщение
    context.user_data['dialog_history'].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })
    
    # Ограничиваем размер истории
    if len(context.user_data['dialog_history']) > max_history:
        context.user_data['dialog_history'] = context.user_data['dialog_history'][-max_history:]


```
project_root/
│
├── main.py                    # Основной файл для запуска бота
├── config.py                  # Конфигурация и константы
├── utils/
│   ├── __init__.py
│   ├── logging_setup.py       # Настройка логирования
│   ├── network.py             # Сетевые утилиты
|   ├── system_monitor.py         # Вывод информации о сервере
│   └── dialog_history.py      # Работа с историей диалогов
├── handlers/
│   ├── __init__.py
│   ├── command_handlers.py    # Обработчики команд
│   ├── message_handlers.py    # Обработчики сообщений
│   ├── callback_handlers.py   # Обработчики кнопок
│   └── error_handlers.py      # Обработчики ошибок
└── services/
    ├── __init__.py
    └── mistral_service.py     # Сервис для работы с Mistral AI
```

# Breww Telegram Bot

Телеграм-бот для магазина чая. Написан на aiogram 3 + SQLAlchemy + SQLite.

## Стек
- Python 3.14
- aiogram 3.28
- SQLAlchemy 2.0 (async)
- aiosqlite
- python-dotenv

## Запуск
1. Клонировать репозиторий
2. Создать виртуальное окружение и установить зависимости:
   pip install -r requirements.txt
3. Создать файл .env на основе .env.example
4. Запустить: python main.py

## Структура
- handlers/ — обработчики сообщений и колбэков
- keyboards/ — клавиатуры
- repositories/ — работа с БД
- database/models/ — модели SQLAlchemy
- filters/ — кастомные фильтры
- states/ — FSM-состояния
- middlewares/ — мидлвари
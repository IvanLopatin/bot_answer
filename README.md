# Telegram Mentor Bot

Это Telegram-бот, который помогает собирать заявки на менторство. Бот задаёт пользователю серию вопросов, аккумулирует ответы с использованием FSM из **aiogram 3.x**, а затем отправляет итоговое сообщение администратору. Для обеспечения работоспособности контейнера используется FastAPI для Health Probe.

## Функциональность

- **Опрос заявок на менторство:** бот последовательно задаёт вопросы и собирает ответы.
- **Использование FSM:** управление состояниями реализовано с помощью aiogram 3.x.
- **Отправка итогового отчёта:** после заполнения формы данные отправляются администратору.
- **Health Probe:** для контроля готовности контейнера реализован HTTP-эндпоинт `/health` с FastAPI.
- **Поддержка Docker:** имеется Dockerfile для сборки контейнера, готового к деплою на облачные платформы (например, Cloud.ru).

## Требования

- Python 3.9 или выше
- [aiogram>=3.0.0b1](https://docs.aiogram.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [uvicorn](https://www.uvicorn.org/)

## Установка

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository
   ```
   
	2.	Создайте и активируйте виртуальное окружение:
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate

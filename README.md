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
ф
2. **Создайте и активируйте виртуальное окружение:**
    ```bash
   python -m venv venv source venv/bin/activate  # Для Windows: venv\Scripts\activate
    ```
    
4. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Конфигурация**

Перед запуском бота необходимо задать следующие переменные окружения или изменить соответствующие константы в коде:
	•	API_TOKEN — токен вашего Telegram-бота, полученный через @BotFather.
	•	ADMIN_CHAT — ID или юзернейм администратора, которому будут отправляться итоговые отчёты (например, @ivan_yas).

6. **Локальный запуск**

Чтобы запустить бота локально, выполните:
```bash 
python bot.py
```

После запуска бот начнёт опрашивать пользователей. Health endpoint будет доступен по адресу http://localhost:8080/health.

**Docker**

Сборка образа

Для сборки Docker-образа используйте следующую команду (с указанием нужной архитектуры):
```bash 
docker build --platform linux/amd64 -t bot_answer3 .
```
6.2. Тегирование образа
```bash
docker tag bot_answer3 botanswer.cr.cloud.ru/bot_answer3:latest
```
6.3. Аутентификация и публикация образа
```bash
docker login botanswer.cr.cloud.ru -u <key_id> -p <key_secret>
docker push botanswer.cr.cloud.ru/bot_answer3:latest
```
7. Развёртывание в Cloud.ru Container Apps
	1.	Войдите в личный кабинет Cloud.ru и перейдите в раздел Container Apps.
	2.	Создайте новое приложение:
	•	Название контейнера: например, bot-answer.
	•	URI образа: botanswer.cr.cloud.ru/bot_answer3:latest.
	•	Порт контейнера: укажите 8080 (порт, на котором работает Health endpoint).
	•	Health Probe: настройте GET-запрос на /health.
	•	Переменные окружения: задайте API_TOKEN и ADMIN_CHAT.
	•	Ресурсы: при необходимости укажите лимиты CPU и памяти.
	3.	Сохраните и запустите приложение.

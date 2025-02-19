# Используем официальный базовый образ Python
FROM python:3.9-slim

# Отключаем создание .pyc файлов и буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости (например, gcc)
RUN apt-get update && apt-get install -y gcc

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем исходный код приложения
COPY . .

# Команда для запуска бота
CMD ["python", "bot.py"]
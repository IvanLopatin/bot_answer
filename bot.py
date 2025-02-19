import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Замените на реальные значения
API_TOKEN = "YOUR_BOT_TOKEN"
ADMIN_CHAT = "@ivan_yas"

# Инициализация бота и хранилища состояний
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Определяем FSM для опроса
class MentorForm(StatesGroup):
    name = State()
    role = State()
    direction = State()
    level = State()
    skills = State()
    goal = State()
    issues = State()
    time = State()
    format = State()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer("Привет! Давай заполним чек-лист для менторства.\nКак тебя зовут?", parse_mode=types.ParseMode.HTML)
    await state.set_state(MentorForm.name)

@dp.message(MentorForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("👤 <b>Кто ты сейчас?</b> (Студент, начинающий специалист, опытный ИТ-специалист и т. д.)", parse_mode=types.ParseMode.HTML)
    await state.set_state(MentorForm.role)

@dp.message(MentorForm.role)
async def process_role(message: types.Message, state: FSMContext):
    await state.update_data(role=message.text)
    await message.answer("💼 <b>Какое направление в ИТ тебе интересно?</b> (Разработка, ИБ, аналитика, DevOps, другое)", parse_mode=types.ParseMode.HTML)
    await state.set_state(MentorForm.direction)

@dp.message(MentorForm.direction)
async def process_direction(message: types.Message, state: FSMContext):
    await state.update_data(direction=message.text)
    await message.answer("🎯 <b>Какой у тебя уровень знаний?</b> (Новичок, знаю основы, есть коммерческий опыт)", parse_mode=types.ParseMode.HTML)
    await state.set_state(MentorForm.level)

@dp.message(MentorForm.level)
async def process_level(message: types.Message, state: FSMContext):
    await state.update_data(level=message.text)
    await message.answer("📊 <b>Какие навыки у тебя уже есть?</b> (Языки программирования, технологии, опыт работы)", parse_mode=types.ParseMode.HTML)
    await state.set_state(MentorForm.skills)

@dp.message(MentorForm.skills)
async def process_skills(message: types.Message, state: FSMContext):
    await state.update_data(skills=message.text)
    await message.answer("🏆 <b>Какая у тебя цель?</b> (Войти в ИТ, сменить работу, получить оффер, прокачать навыки)", parse_mode=types.ParseMode.HTML)
    await state.set_state(MentorForm.goal)

@dp.message(MentorForm.goal)
async def process_goal(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await message.answer("⚠️ <b>Какие проблемы мешают двигаться дальше?</b> (Не знаю, с чего начать / нет практики / не прохожу собеседования)", parse_mode=types.ParseMode.HTML)
    await state.set_state(MentorForm.issues)

@dp.message(MentorForm.issues)
async def process_issues(message: types.Message, state: FSMContext):
    await state.update_data(issues=message.text)
    await message.answer("⏳ <b>Сколько времени готов уделять обучению?</b> (1-2 часа в день, 5+ часов в неделю и т. д.)", parse_mode=types.ParseMode.HTML)
    await state.set_state(MentorForm.time)

@dp.message(MentorForm.time)
async def process_time(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer("📞 <b>Какой формат менторства тебе удобен?</b> (Чат, созвоны, разбор задач, работа над проектом)", parse_mode=types.ParseMode.HTML)
    await state.set_state(MentorForm.format)

@dp.message(MentorForm.format)
async def process_format(message: types.Message, state: FSMContext):
    await state.update_data(format=message.text)
    data = await state.get_data()
    # Формируем итоговое сообщение с HTML-форматированием и эмодзи
    result_text = (
        "<b>Новая заявка на менторство!</b>\n\n"
        f"👤 <b>Имя:</b> {data.get('name')}\n"
        f"💼 <b>Кто сейчас:</b> {data.get('role')}\n"
        f"🎯 <b>Направление:</b> {data.get('direction')}\n"
        f"📊 <b>Уровень знаний:</b> {data.get('level')}\n"
        f"🛠 <b>Навыки:</b> {data.get('skills')}\n"
        f"🏆 <b>Цель:</b> {data.get('goal')}\n"
        f"⚠️ <b>Проблемы:</b> {data.get('issues')}\n"
        f"⏳ <b>Время на обучение:</b> {data.get('time')}\n"
        f"📞 <b>Формат менторства:</b> {data.get('format')}\n"
    )
    # Отправляем итоговое сообщение админу с HTML-форматированием
    await bot.send_message(ADMIN_CHAT, result_text, parse_mode=types.ParseMode.HTML)
    # Отправляем пользователю сообщение о завершении
    await message.answer("✅ Данные отправлены ментору. Спасибо!", parse_mode=types.ParseMode.HTML)
    await state.clear()

# Реализация Health Probe через FastAPI
from fastapi import FastAPI
from fastapi.responses import JSONResponse

health_app = FastAPI()

@health_app.get("/health")
async def health():
    return JSONResponse(content={"status": "ok"})

# Основная функция: запускаем бота и HTTP-сервер параллельно
import uvicorn

async def main():
    # Создаем две задачи: polling бота и uvicorn для FastAPI
    bot_task = asyncio.create_task(dp.start_polling(bot))
    config = uvicorn.Config(health_app, host="0.0.0.0", port=8080, log_level="info")
    server = uvicorn.Server(config)
    health_task = asyncio.create_task(server.serve())
    await asyncio.gather(bot_task, health_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception("Error in main: %s", e)
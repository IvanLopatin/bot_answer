import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен и идентификатор чата администратора
API_TOKEN = "7587439282:AAGXUVVsgplLLU3pD0K1hn5JQThMoUY20Jk"
ADMIN_CHAT = 1270626619

# Инициализация бота, хранилища и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

submitted_applications = {}


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


async def set_commands():
    commands = [
        BotCommand(command="start", description="Начать заполнение заявки"),
        BotCommand(command="restart", description="Сбросить заявку и начать заново"),
        BotCommand(command="check", description="Проверить отправленную заявку"),
        BotCommand(command="help", description="Список команд"),
    ]
    await bot.set_my_commands(commands)


def is_command(text: str) -> bool:
    """Проверяет, начинается ли текст с символа '/'."""
    return text.strip().startswith("/")


# Глобальный обработчик команды /help (без дополнительных аргументов)
@dp.message(Command("help"))
async def help_handler(message: types.Message, state: FSMContext):
    await state.clear()
    help_text = (
        "<b>Список команд:</b>\n\n"
        "/start – начать заполнение заявки\n"
        "/restart – сбросить заявку и начать заново\n"
        "/check – проверить отправленную заявку\n"
        "/help – показать это сообщение"
    )
    await message.answer(help_text, parse_mode=ParseMode.HTML)


@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    welcome_text = (
        "Добро пожаловать в бота для подачи заявки на менторство!\n"
        "Здесь вы сможете заполнить анкету, после чего заявка будет отправлена нашему ментору.\n\n"
        "Давайте начнем!\n\n"
        "Как тебя зовут?"
    )
    await state.set_state(MentorForm.name)
    await message.answer(welcome_text, parse_mode=ParseMode.HTML)


@dp.message(Command("restart"))
async def restart_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Сброс заявки. Начинаем сначала.\nКак тебя зовут?", parse_mode=ParseMode.HTML)
    await state.set_state(MentorForm.name)


@dp.message(Command("check"))
async def check_handler(message: types.Message):
    chat_id = message.chat.id
    if chat_id in submitted_applications:
        data = submitted_applications[chat_id]
        result_text = (
            "<b>Ваша заявка на менторство:</b>\n\n"
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
        await message.answer(result_text, parse_mode=ParseMode.HTML)
    else:
        await message.answer("Заявка ещё не отправлена. Заполните её командой /start.")


# Обработчики для состояний с проверкой на команды
@dp.message(MentorForm.name)
async def process_name(message: types.Message, state: FSMContext):
    if is_command(message.text):
        await message.answer("Команды в процессе заполнения анкеты не принимаются. Пожалуйста, введите ваше имя.")
        return
    await state.update_data(name=message.text)
    await message.answer(
        "👤 <b>Кто ты сейчас?</b> (Студент, начинающий специалист, опытный ИТ-специалист и т. д.)",
        parse_mode=ParseMode.HTML
    )
    await state.set_state(MentorForm.role)


@dp.message(MentorForm.role)
async def process_role(message: types.Message, state: FSMContext):
    if is_command(message.text):
        await message.answer("Команды в процессе заполнения анкеты не принимаются. Пожалуйста, введите вашу роль.")
        return
    await state.update_data(role=message.text)
    await message.answer(
        "💼 <b>Какое направление в ИТ тебе интересно?</b> (Разработка, ИБ, аналитика, DevOps, другое)",
        parse_mode=ParseMode.HTML
    )
    await state.set_state(MentorForm.direction)


@dp.message(MentorForm.direction)
async def process_direction(message: types.Message, state: FSMContext):
    if is_command(message.text):
        await message.answer(
            "Команды в процессе заполнения анкеты не принимаются. Пожалуйста, введите направление в ИТ.")
        return
    await state.update_data(direction=message.text)
    await message.answer(
        "🎯 <b>Какой у тебя уровень знаний?</b> (Новичок, знаю основы, есть коммерческий опыт)",
        parse_mode=ParseMode.HTML
    )
    await state.set_state(MentorForm.level)


@dp.message(MentorForm.level)
async def process_level(message: types.Message, state: FSMContext):
    if is_command(message.text):
        await message.answer(
            "Команды в процессе заполнения анкеты не принимаются. Пожалуйста, введите ваш уровень знаний.")
        return
    await state.update_data(level=message.text)
    await message.answer(
        "📊 <b>Какие навыки у тебя уже есть?</b> (Языки программирования, технологии, опыт работы)",
        parse_mode=ParseMode.HTML
    )
    await state.set_state(MentorForm.skills)


@dp.message(MentorForm.skills)
async def process_skills(message: types.Message, state: FSMContext):
    if is_command(message.text):
        await message.answer("Команды в процессе заполнения анкеты не принимаются. Пожалуйста, введите ваши навыки.")
        return
    await state.update_data(skills=message.text)
    await message.answer(
        "🏆 <b>Какая у тебя цель?</b> (Войти в ИТ, сменить работу, получить оффер, прокачать навыки)",
        parse_mode=ParseMode.HTML
    )
    await state.set_state(MentorForm.goal)


@dp.message(MentorForm.goal)
async def process_goal(message: types.Message, state: FSMContext):
    if is_command(message.text):
        await message.answer("Команды в процессе заполнения анкеты не принимаются. Пожалуйста, введите вашу цель.")
        return
    await state.update_data(goal=message.text)
    await message.answer(
        "⚠️ <b>Какие проблемы мешают двигаться дальше?</b> (Не знаю, с чего начать / нет практики / не прохожу собеседования)",
        parse_mode=ParseMode.HTML
    )
    await state.set_state(MentorForm.issues)


@dp.message(MentorForm.issues)
async def process_issues(message: types.Message, state: FSMContext):
    if is_command(message.text):
        await message.answer("Команды в процессе заполнения анкеты не принимаются. Пожалуйста, опишите проблемы.")
        return
    await state.update_data(issues=message.text)
    await message.answer(
        "⏳ <b>Сколько времени готов уделять обучению?</b> (1-2 часа в день, 5+ часов в неделю и т. д.)",
        parse_mode=ParseMode.HTML
    )
    await state.set_state(MentorForm.time)


@dp.message(MentorForm.time)
async def process_time(message: types.Message, state: FSMContext):
    if is_command(message.text):
        await message.answer(
            "Команды в процессе заполнения анкеты не принимаются. Пожалуйста, введите время, которое вы готовы уделять обучению.")
        return
    await state.update_data(time=message.text)
    await message.answer(
        "📞 <b>Какой формат менторства тебе удобен?</b> (Чат, созвоны, разбор задач, работа над проектом)",
        parse_mode=ParseMode.HTML
    )
    await state.set_state(MentorForm.format)


@dp.message(MentorForm.format)
async def process_format(message: types.Message, state: FSMContext):
    if is_command(message.text):
        await message.answer(
            "Команды в процессе заполнения анкеты не принимаются. Пожалуйста, введите формат менторства.")
        return
    await state.update_data(format=message.text)
    data = await state.get_data()

    user_first_name = message.from_user.first_name or "Неизвестно"
    user_username = f"@{message.from_user.username}" if message.from_user.username else ""

    result_text = (
        f"<b>Новая заявка на менторство от пользователя {user_first_name} {user_username}!</b>\n\n"
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
    submitted_applications[message.chat.id] = data
    await bot.send_message(ADMIN_CHAT, result_text, parse_mode=ParseMode.HTML)
    await message.answer("✅ Данные отправлены ментору. Спасибо!", parse_mode=ParseMode.HTML)
    await state.clear()


# Реализация Health Probe через FastAPI
from fastapi import FastAPI
from fastapi.responses import JSONResponse

health_app = FastAPI()


@health_app.get("/health")
async def health():
    return JSONResponse(content={"status": "ok"})


import uvicorn


async def main():
    await set_commands()
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

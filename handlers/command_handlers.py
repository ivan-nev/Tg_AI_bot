from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.states import Profile
from utils import AI
from keyboards import create_menu_inline

router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    start_text = '''Привет! Я бот, твой помощник.
    Выбери тему из меню'''
    await message.answer(text=start_text, reply_markup=create_menu_inline())
    await state.clear()

@router.message(Command('about'))
async def about(message: Message):
    await message.answer(text=(
        "🤖 <b>О боте</b>\n\n"
        "Этот бот — твой умный и остроумный собеседник, "
        "помощник и развлечение в одном лице! 🎯\n\n"
        "Вот что он умеет:\n"
        "• 💡 Рассказывать рандомные факты\n"
        "• 🤖 Общаться через ChatGPT\n"
        "• 💬 Вести диалог от лица знаменитостей\n"
        "• 🎯 Проводить квизы по разным темам\n"
        "• 🔤 Переводить тексты\n"
        "• 📋 Помогать составлять резюме\n\n"
        "Создан с ❤️ для любознательных и активных.\n"
        "Погружайся — будет интересно! 🚀\n"
        "/start - Начать диалог\n"
    ))

@router.message(Command('help'))
async def help_handler(message: Message):
    help_text = (
        "📘 <b>Справка по командам</b>\n\n"
        "/start — Запустить бота\n"
        "/help — Показать эту подсказку\n"
        "/about — Узнать больше о боте\n\n"
        "Используй меню для навигации — "
        "там ты найдёшь все доступные функции! 💡"
    )
    await message.answer(help_text)

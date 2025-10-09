from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import ADMIN_IDS
from keyboards.admin_kb.admin_kb import *
from keyboards.client_kb import *
from database.client_db import *
from handlers.client import RegState  # используем состояния клиента


router = Router()

WELCOME_TEXT = (
    "🇺🇿 Assalomu alaykum! Bizning xizmatimizga xush kelibsiz 🚗✨\n"
    "🇷🇺 Здравствуйте! Добро пожаловать в наш сервис 🚗✨\n"
    "🇬🇧 Hello! Welcome to our service 🚗✨\n\n"
)

@router.message(Command("start"))
async def start_entry(message: Message, state: FSMContext):
    user_id = message.from_user.id

    # ❌ Сбрасываем состояния (перезапуск)
    await state.clear()

    # 1) Админ → показываем админ-меню
    if user_id in ADMIN_IDS:
        await message.answer(
            "🔑 Привет, админ! Панель управления готова.",
            reply_markup=get_admin_main_menu()
        )
        return

    # 2) Любой клиент → всегда как первый запуск
    await message.answer(WELCOME_TEXT, reply_markup=get_lang_kb())
    await state.set_state(RegState.lang)


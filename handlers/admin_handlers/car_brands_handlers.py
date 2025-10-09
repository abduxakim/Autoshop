from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.admin_kb.car_brands_kb import get_car_brands_kb
from keyboards.admin_kb.admin_kb import get_admin_main_menu

from database.admin_db.car_brands_db import add_car_brands

from handlers.admin_handlers.admin_main_handlers import BACK_STACKS



admin_car_brands_router = Router()



class AddCarBrands(StatesGroup):
    name = State()

# Показать все категории -> список категорий, при возврате хотим попасть в "action"
@admin_car_brands_router.message(F.text == "📂 Показать бренды авто")
async def show_all_categories(message: Message):
    user = message.from_user.id
    BACK_STACKS[user].append("actaction_categoriesion")   # parent of categories = action
    await message.answer("Вот список брендов авто  📂", reply_markup=get_car_brands_kb("name"))


# 1. Запрашиваем название бренда
@admin_car_brands_router.message(F.text == "➕ Добавить бренд авто")
async def add_car_brands_handler(message:Message,state:FSMContext):
    await message.answer("Введите название бренда авто")
    await state.set_state(AddCarBrands.name)

# 2. Получаем название и сохраняем в БД
@admin_car_brands_router.message(AddCarBrands.name)
async def save_car_brands_name(message: Message, state: FSMContext):
    name = message.text.strip()

    if not name or name == "-":
        await message.answer("❌ Название бренда не может быть пустым. Попробуйте ещё раз.")
        return

    add_car_brands(name)

    await message.answer(
        f"✅ Бренд авто успешно добавлен:\n\n"
        f"🚗 {name}",
        reply_markup=get_admin_main_menu()
    )
    await state.clear()









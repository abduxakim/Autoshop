#TODO fix back stack for car brands
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.admin_kb.car_brands_kb import (
    get_car_brands_kb,
    get_car_brands_action_kb,                                            
)


from database.admin_db.car_brands_db import add_car_brands

from handlers.admin_handlers.admin_main_handlers import BACK_STACKS



admin_car_brands_router = Router()



class AddCarBrands(StatesGroup):
    name = State()


# --- Показать бренды ---
@admin_car_brands_router.message(F.data == "brands_menu")
async def brands_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "🚘 Управление брендами авто:",
        reply_markup=get_car_brands_action_kb()
    )
    await callback.answer()

# ============= Показ списка брендов =============
@admin_car_brands_router.callback_query(F.data == "show_brands")
async def show_car_brands(callback: CallbackQuery):
    await callback.message.edit_text(
        "📋 Список брендов:",
        reply_markup=get_car_brands_kb()
    )
    await callback.answer()




# --- Добавить бренд ---
@admin_car_brands_router.callback_query(F.data == "add_brand")
async def add_brand(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text("Введите название нового бренда:")
    await state.set_state(AddCarBrands.name)
    await callback.answer()


# 2. Получаем название и сохраняем в БД
@admin_car_brands_router.message(AddCarBrands.name)
async def save_brand_name(message:Message,state:FSMContext):
    name = message.text.strip()
    if not name or name == "-":
        await message.answer("❌ Название бренда не может быть пустым. Попробуйте ещё раз.")
        return
    add_car_brands(name)  

    await message.answer  (
        f"✅ Бренд авто успешно добавлен:\n\n"
        f"🚗 {name}",
        reply_markup=get_car_brands_action_kb()
    )       
    await state.clear()





    










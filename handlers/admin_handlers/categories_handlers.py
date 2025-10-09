# handlers/admin_handlers/categories_handlers.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter

# --- Импорт клавиатур ---
from keyboards.admin_kb.admin_kb import get_admin_main_menu
from keyboards.admin_kb.categories_kb import (
    build_categories_kb,
    update_category_choose_lang_kb,
    get_category_action_kb,
    get_post_delete_kb,
    get_confirm_delete_kb
)
from keyboards.admin_kb.car_brands_kb import get_car_brands_action_kb

# --- Импорт функций работы с базой ---
from database.admin_db.categories_db import (
    add_category,
    get_categories,
    delete_category,
    update_category_field,
)

# --- Импорт вспомогательных данных ---
from handlers.admin_handlers.admin_main_handlers import BACK_STACKS


# -------------------------------------------------
#   Router для админских категорий
# -------------------------------------------------
admin_categories_router = Router()


# -------------------------------------------------
#   FSM состояния для добавления категории
# -------------------------------------------------
class AddCategory(StatesGroup):
    """Состояния для поэтапного добавления новой категории"""
    name_ru = State()
    name_en = State()
    name_uz = State()


# =================================================
#   ПОКАЗАТЬ КАТЕГОРИИ
# =================================================
@admin_categories_router.message(F.text == "📂 Показать категории товаров")
async def show_all_categories(message: Message):
    """
    Показывает администратору список всех категорий для управления (Update/Delete)
    """
    user_id = message.from_user.id
    BACK_STACKS[user_id].append("action_categories")

    await message.answer(
        "Вот список категорий 📂",
        reply_markup=build_categories_kb(action="manage", lang="ru")
    )


@admin_categories_router.callback_query(F.data.startswith("choose_cat:"))
async def choose_car_brand(callback: CallbackQuery, state: FSMContext):
    """
    После выбора категории — предлагаем выбрать марку автомобиля.
    """
    # Если пользователь находится в состоянии FSM — игнорируем
    if await state.get_state() is not None:
        await callback.answer()
        return

    category_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id
    BACK_STACKS[user_id].append("categories")

    await callback.message.edit_text(
        "Выберите марку автомобиля 🚘:",
        reply_markup=get_car_brands_action_kb()
    )
    await callback.answer()





# =================================================
#   ДОБАВИТЬ КАТЕГОРИЮ 
# =================================================
#ДЛЯ НЕГО ОТМЕНА РАБОТАЕТ ЧЕРЕЗ @admin_main_router.callback_query(F.data.startswith("back:"))async def go_back_inline
@admin_categories_router.message(F.text == "➕ Добавить категорию")
async def add_category_start(message: Message, state: FSMContext):
    """Запрашиваем название категории на русском"""
    await message.answer("Введите название категории на русском 🇷🇺:")
    await state.set_state(AddCategory.name_ru)


@admin_categories_router.message(AddCategory.name_ru)
async def add_category_ru(message: Message, state: FSMContext):
    """Получаем русское название"""
    await state.update_data(name_ru=message.text)
    await message.answer("Введите название категории на английском 🇬🇧 (или '-' если нет):")
    await state.set_state(AddCategory.name_en)


@admin_categories_router.message(AddCategory.name_en)
async def add_category_en(message: Message, state: FSMContext):
    """Получаем английское название"""
    name_en = None if message.text.strip() == "-" else message.text.strip()
    await state.update_data(name_en=name_en)
    await message.answer("Введите название категории на узбекском 🇺🇿 (или '-' если нет):")
    await state.set_state(AddCategory.name_uz)


@admin_categories_router.message(AddCategory.name_uz)
async def add_category_uz(message: Message, state: FSMContext):
    """Получаем узбекское название и сохраняем категорию в БД"""
    name_uz = None if message.text.strip() == "-" else message.text.strip()
    data = await state.get_data()

    name_ru = data["name_ru"]
    name_en = data["name_en"]

    add_category(name_ru, name_en, name_uz)

    await message.answer(
        f"✅ Категория добавлена:\n\n"
        f"🇷🇺 {name_ru}\n"
        f"🇬🇧 {name_en or '—'}\n"
        f"🇺🇿 {name_uz or '—'}",
        reply_markup=get_admin_main_menu()
    )
    await state.clear()


# =================================================
#   УДАЛИТЬ КАТЕГОРИЮ
# =================================================
"""@admin_categories_router.message(F.text == "🗑️ Удалить категорию")
async def delete_category_handler(message: Message, state: FSMContext):
    ""Показывает список категорий для удаления""
    kb = build_categories_kb(action="delete")
    await message.answer("Выберите категорию для удаления:", reply_markup=kb)"""


# Нажали на 🗑 — спрашиваем подтверждение
@admin_categories_router.callback_query(F.data.startswith("delete_cat:"))
async def confirm_delete_category(callback: CallbackQuery):
    cat_id = int(callback.data.split(":")[1])
    categories = get_categories()
    category = next((c for c in categories if c["id"] == cat_id), None)

    if not category:
        await callback.answer("❌ Категория не найдена.", show_alert=True)
        return

    await callback.message.edit_text(
        f"❗ Вы уверены, что хотите удалить категорию <b>{category['name_ru']}</b>?",
        reply_markup=get_confirm_delete_kb(cat_id),
        parse_mode="HTML"
    )


# Подтверждение удаления
@admin_categories_router.callback_query(F.data.startswith("confirm_delete:"))
async def process_delete_category(callback: CallbackQuery):
    cat_id = int(callback.data.split(":")[1])
    categories = get_categories()
    category = next((c for c in categories if c["id"] == cat_id), None)

    if not category:
        await callback.answer("❌ Категория не найдена.", show_alert=True)
        return

    # Удаляем
    delete_category(category["id"], category["name_ru"])

    # Показываем обновлённый список
    keyboard = get_post_delete_kb()

    if not keyboard:
        await callback.message.edit_text("✅ Все категории удалены.")
    else:
        await callback.message.edit_text(
            f"✅ Категория <b>{category['name_ru']}</b> удалена.\n\nВыберите следующую категорию:",
            reply_markup=keyboard,
            parse_mode="HTML"
        )



# =================================================
#   ОБНОВИТЬ КАТЕГОРИЮ
# =================================================
@admin_categories_router.message(F.text == "♻️ Обновить категорию")
async def process_update_category(message: Message):
    """Показывает список категорий для обновления"""
    kb = build_categories_kb(action="update")
    await message.answer("Выберите категорию для редактирования:", reply_markup=kb)


@admin_categories_router.callback_query(F.data.startswith("update_cat:"))
async def update_category_choose_lang(callback: CallbackQuery, state: FSMContext):
    """Выбор языка для обновления категории"""
    category_id = int(callback.data.split(":")[1])
    await state.update_data(category_id=category_id)

    await callback.message.edit_text(
        "Выберите язык, который хотите обновить:",
        reply_markup=update_category_choose_lang_kb()
    )
    await callback.answer()


@admin_categories_router.callback_query(F.data.startswith("update_lang:"))
async def update_category_wait_name(callback: CallbackQuery, state: FSMContext):
    """После выбора языка ожидаем новое название категории"""
    lang = callback.data.split(":")[1]
    await state.update_data(update_lang=lang)

    lang_names = {"ru": "русский", "en": "английский", "uz": "узбекский"}
    await callback.message.answer(f"Введите новое название категории ({lang_names[lang]}):")

    await state.set_state("update_category_name")
    await callback.answer()


@admin_categories_router.message(StateFilter("update_category_name"))
async def save_updated_category(message: Message, state: FSMContext):
    """Сохраняет новое название категории"""
    data = await state.get_data()
    category_id = data.get("category_id")
    lang = data.get("update_lang")
    new_name = message.text.strip()

    if not new_name:
        await message.answer("❌ Название не может быть пустым. Попробуйте ещё раз.")
        return

    success = update_category_field(category_id, lang, new_name)

    if success:
        await message.answer(f"✅ Категория успешно обновлена на {lang.upper()}: {new_name}")
    else:
        await message.answer("❌ Ошибка при обновлении категории. Попробуйте позже.")

    await state.clear()


# =================================================
#   ОТМЕНА ЛЮБОГО ДЕЙСТВИЯ 
# =================================================

@admin_categories_router.callback_query(F.data.startswith("cancel_"))
async def cancel_any_action(callback: CallbackQuery, state: FSMContext):
    """
    Универсальная отмена для действий с категориями:
    cancel_delete, cancel_update, cancel_manage и т.д.
    """
    # На всякий случай очищаем состояние (если был FSM)
    await state.clear()

    # Удаляем текущее сообщение
    await callback.message.delete()

    # Возвращаем меню действий с категориями
    await callback.message.answer(
        "❌ Действие отменено.",
        reply_markup=get_category_action_kb()
    )

    await callback.answer()

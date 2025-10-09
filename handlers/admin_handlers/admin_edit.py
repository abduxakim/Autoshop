import os,re
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message,  CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import ADMIN_IDS
from database.admin_db import *
from database.common_db import *
from keyboards.admin_kb.admin_kb import *



router = Router()

"""#FSM Context
# Описываем группу состояний для обновления 
class UPDATE(StatesGroup):
    name = State()
    desc = State()
    price = State()
    qty = State()
    photo_path = State()"""


"""# --- 1. Список товаров ---
@router.message(Command("products"))
async def list_products(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    product_list = get_all_products()
    if not product_list:
        await message.answer("📦 Список товаров пуст.")
        return

    await message.answer(
        "📋 Выберите товар для редактирования:",
        reply_markup=get_products_kb(product_list)
    )
"""




"""
# ---  Показ подробной информации о товаре ---
@router.callback_query(F.data.startswith("view_product:"))
async def show_product_details(callback: CallbackQuery):
    pid = int(callback.data.split(":")[1])
    product = get_product_by_id(pid)  # нужно будет добавить в db.py

    if not product:
        await callback.answer("❌ Товар не найден.", show_alert=True)
        return

    text = (
        f"🆔 {product['id']}\n"
        f"📦 Название: {product['name']}\n"
        f"💬 Описание: {product['description']}\n"
        f"💰 Цена: {product['price']} ₽\n"
        f"📦 Кол-во: {product['qty']} шт"
    )

    await callback.message.edit_text(text, reply_markup=get_product_actions_kb(pid))


# --- 2. Удаление товара ---
@router.callback_query(F.data.startswith("delete_product:"))
async def process_delete_product(callback: CallbackQuery):
    pid = int(callback.data.split(":")[1])

    # Получаем путь к фото из БД и удаляем фото
    product = get_product_by_id(pid)
    if product["photo_path"] and os.path.exists(product["photo_path"]):
        os.remove(product["photo_path"])

    # Удаляем товар из БД
    delete_product(pid)

  
    await callback.answer("🗑 Товар удалён.")

    # Обновляем список товаров
    products = get_all_products()
    if products:
        await callback.message.edit_text(
            "📋 Выберите товар:",
            reply_markup=get_products_kb(products)
        )
    else:
        await callback.message.edit_text("📦 Список товаров пуст.")


# --- 3. Обновление товара ---
@router.callback_query(F.data.startswith("choose_edit_field:"))
async def choose_edit_field(callback: CallbackQuery):
    pid = int(callback.data.split(":")[1])
    await callback.message.edit_text(
        "⚙ Что хотите изменить?",
        reply_markup=get_update_fields_kb(pid)
    )

# Название
@router.callback_query(F.data.startswith("edit_name:"))
async def edit_name(callback: CallbackQuery, state: FSMContext):
    pid = int(callback.data.split(":")[1])
    await state.update_data(product_id=pid)
    await callback.message.answer("✏ Введите новое название:")
    await state.set_state(UPDATE.name)


@router.message(UPDATE.name)
async def save_name(message: Message, state: FSMContext):
    data = await state.get_data()
    pid = data["product_id"]
    update_product(pid, name=message.text,
                   description=get_product_by_id(pid)["description"],
                   price=get_product_by_id(pid)["price"],
                   qty=get_product_by_id(pid)["qty"],
                   photo_path=get_product_by_id(pid)["photo_path"])
    await message.answer("✅ Название обновлено!")
    await state.clear()


# Описание
@router.callback_query(F.data.startswith("edit_desc:"))
async def edit_desc(callback: CallbackQuery, state: FSMContext):
    pid = int(callback.data.split(":")[1])
    await state.update_data(product_id=pid)
    await callback.message.answer("📝 Введите новое описание:")
    await state.set_state(UPDATE.desc)


@router.message(UPDATE.desc)
async def save_desc(message: Message, state: FSMContext):
    data = await state.get_data()
    pid = data["product_id"]
    product = get_product_by_id(pid)
    update_product(pid,
                   name=product["name"],
                   description=message.text,
                   price=product["price"],
                   qty=product["qty"],
                   photo_path=product["photo_path"])
    await message.answer("✅ Описание обновлено!")
    await state.clear()


# Цена
@router.callback_query(F.data.startswith("edit_price:"))
async def edit_price(callback: CallbackQuery, state: FSMContext):
    pid = int(callback.data.split(":")[1])
    await state.update_data(product_id=pid)
    await callback.message.answer("💰 Введите новую цену:")
    await state.set_state(UPDATE.price)


@router.message(UPDATE.price)
async def save_price(message: Message, state: FSMContext):
    data = await state.get_data()
    pid = data["product_id"]

    try:
        price = float(message.text)
    except ValueError:
        await message.answer("❌ Введите корректное число")
        return

    product = get_product_by_id(pid)
    update_product(pid,
                   name=product["name"],
                   description=product["description"],
                   price=price,
                   qty=product["qty"],
                   photo_path=product["photo_path"])
    await message.answer("✅ Цена обновлена!")
    await state.clear()


# Количество
@router.callback_query(F.data.startswith("edit_qty:"))
async def edit_qty(callback: CallbackQuery, state: FSMContext):
    pid = int(callback.data.split(":")[1])
    await state.update_data(product_id=pid)
    await callback.message.answer("📦 Введите новое количество:")
    await state.set_state(UPDATE.qty)


@router.message(UPDATE.qty)
async def save_qty(message: Message, state: FSMContext):
    data = await state.get_data()
    pid = data["product_id"]

    if not message.text.isdigit():
        await message.answer("❌ Введите целое число")
        return

    product = get_product_by_id(pid)
    update_product(pid,
                   name=product["name"],
                   description=product["description"],
                   price=product["price"],
                   qty=int(message.text),
                   photo_path=product["photo_path"])
    await message.answer("✅ Количество обновлено!")
    await state.clear()


# Фото
@router.callback_query(F.data.startswith("edit_photo:"))
async def edit_photo(callback: CallbackQuery, state: FSMContext):
    pid = int(callback.data.split(":")[1])
    product = get_product_by_id(pid)
    #обновляем также по name так как раньше было тока по pid
    await state.update_data(product_id=pid, product_name=product["name"]) 
    await callback.message.answer("📸 Отправьте новое фото товара:")
    await state.set_state(UPDATE.photo_path)


@router.message(UPDATE.photo_path)
async def save_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    pid = data["product_id"]
    product_name = data["product_name"]

     # Удаляем старое фото, если было
    product = get_product_by_id(pid)

    if product["photo_path"] and os.path.exists(product["photo_path"]):
        os.remove(product["photo_path"])

    if not message.photo:
        await message.answer("❌ Пришлите фото")
        return

    file_id = message.photo[-1].file_id
    file = await message.bot.get_file(file_id)

    # Делаем имя файла безопасным
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', product_name)
    photo_path = f"product_images/{safe_name}.jpg"

    await message.bot.download_file(file.file_path, photo_path)

    update_product(pid,
                   name=product["name"],
                   description=product["description"],
                   price=product["price"],
                   qty=product["qty"],
                   photo_path=photo_path)
    await message.answer("✅ Фото обновлено!")
    await state.clear()
"""




"""# Список категорий для удаления
def get_delete_category_kb(lang="ru"):
    categories = get_categories()
    if not categories:
        return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="❌ Нет категорий", callback_data="noop")]]
        )

    keyboard = []
    row = []
    for i, cat in enumerate(categories, start=1):
        text = cat.get(f"name_{lang}", cat["name_ru"])
        row.append(InlineKeyboardButton(text=text, callback_data=f"delete_cat:{cat['id']}"))
        if i % 2 == 0:  # каждые 2 кнопки — новая строка
            keyboard.append(row)
            row = []
    if row:  # остатки (если нечётное кол-во)
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_delete")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

#Список категорий для обновленя
def get_update_category_kb(lang="ru"):
    categories = get_categories()
    if not categories:
        return InlineKeyboardMarkup(
            inline_keyboard= [[InlineKeyboardButton(text="❌ Нет категорий", callback_data="noop")]]
        )
    
    keyboard = []
    row = []
    for i, cat in enumerate(categories, start=1):
        text = cat.get(f"name_{lang}", cat["name_ru"])
        row.append(InlineKeyboardButton(text=text, callback_data=f"update_cat:{cat['id']}"))
        if i % 2 == 0:  # каждые 2 кнопки — новая строка
            keyboard.append(row)
            row = []
    if row:  # остатки (если нечётное кол-во)
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_update")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)"""
